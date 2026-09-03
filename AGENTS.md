# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`llm_translator` is a local (offline-capable) Japanese → English translation CLI. It exists so that confidential documents can be translated without sending them to a hosted service. Its main job is translating DocFX-style HTML API docs and XML files in bulk while preserving markup.

## Commands

The project uses **uv** (the README's poetry instructions are stale — the repo migrated to uv in `48c797c`).

```shell
uv sync                                     # install deps (incl. dev group)
uv run python -m llm_translator --version
uv run python -m llm_translator --text "これは日本語です"
uv run python -m llm_translator --file ./samples/index.html
uv run python -m llm_translator --dir ./samples

uv run ruff check .                         # lint
uv run ruff format .                        # format

uv build                                    # build wheel + sdist into dist/
uv publish --index JEOL-PyPI                # private Azure Artifacts feed
```

`uv publish` authenticates through keyring; set this up first:

```shell
uv tool install keyring --with artifacts-keyring
export UV_KEYRING_PROVIDER=subprocess       # artifacts-keyring supplies the token as the password
export UV_PUBLISH_USERNAME=VssSessionToken
```

`uv publish` reads credentials **only** from `UV_PUBLISH_USERNAME` / `UV_PUBLISH_PASSWORD` /
`UV_PUBLISH_TOKEN` (or the matching `--username` / `--password` / `--token` flags). It ignores the
`UV_INDEX_*` variables even when `--index` names the index — those apply to *resolving from* an
index, not *uploading to* it. `README.md` documents `UV_INDEX_PRIVATE_REGISTRY_USERNAME` here,
which is wrong twice over: wrong variable family, and a placeholder index name copied from uv's
docs. With it, uv reports "Neither credentials nor keyring are configured" and falls through to
trusted publishing, which fails against Azure Artifacts.

To *install* from the private feed, the index-scoped form is the correct one:
`UV_INDEX_JEOL_PYPI_USERNAME` — the index name uppercased with `-` replaced by `_`.

There is **no test framework** configured (no pytest, no test suite). `src/llm_translator/test_cuda.py` is a standalone GPU-diagnostic script (`uv run python -m llm_translator.test_cuda`), not a unit test. `sample.py` and `soup_test/*.py` are likewise scratch scripts run directly, and they assume the repo root as CWD.

`--version` reads installed package metadata, so it requires the package to be installed (`uv sync` does this via the editable install).

## Architecture

Layered, one direction only: CLI → application → domain → model.

```
__main__.py            fire-based CLI (--text / --file / --dir / --version); loads .env
application/           TranslateService — orchestration, file discovery, output paths
domain/html_translator HtmlTranslator — BeautifulSoup "html.parser"
domain/translator/     Translator (model façade) + XmlTranslator ("lxml-xml")
domain/translator/models/  ModelBase + MbartModel / NLLBModel / GemmaModel
domain/file_finder/    FileFinder — rglob over extension patterns
```

**Swapping the translation model** happens in exactly one place: `domain/translator/__init__.py`. `Translator.__init__` imports the concrete model class *inside the constructor* — this is deliberate (loading transformers/model weights at module import made startup unacceptably slow, see `99b9e02`). Three `ModelBase` implementations exist; only one is wired at a time and the others are left as commented-out imports. Keep the lazy-import pattern when changing models.

**Batch translation contract.** Both `HtmlTranslator` and `XmlTranslator` follow the same three-step shape: collect `(text, node)` pairs → one `translator.translate(list[str])` call → `zip` results back onto nodes. The pairing relies on the model returning results in input order, one output per input. Any new `ModelBase` implementation must preserve that invariant.

**What gets translated.** `_contains_japanese` (duplicated in both translators) gates every node — only text containing kana or CJK is sent to the model. `HtmlTranslator` additionally only descends into `<article>` elements and skips `script`, `style`, `code`, `h4`, `h5`, `h6`; these exclusions are tuned for DocFX output (headings there hold namespaces/signatures, not prose).

**Output layout.** `--file foo.html` writes a sibling `foo.en.html`. `--dir samples` mirrors the tree into a sibling `samples.en/`. `FileFinder` skips any path whose first path segment starts with `en`, so previously generated output nested under the source tree is not re-translated.

**Model differences.** `MbartModel` (current) translates one string per `generate()` call — no batching. `NLLBModel` and `GemmaModel` size batches dynamically from free CUDA memory via `_get_optimal_batch_size()`. All three move to CUDA when available and fall back to CPU otherwise. `GemmaModel` calls `huggingface_hub.login()` **at module import time** using `HUGGING_FACE_API_KEY` from `.env` — importing that module without the key set will fail, which is why the import is inside `Translator.__init__` rather than at the top of the package.

## Conventions

- Commit messages use an uppercase type prefix: `FEAT:`, `FIX:`, `MAINT:`, `DOC:`, `BUMP:`. Subject text is often Japanese; either language is fine.
- Source files are read as `utf-8-sig` (input docs carry BOMs) and written as `utf-8`.
- Code comments are written in Japanese; match that when editing existing files.
- A `Logger` is threaded through as `Optional[Logger]` — every use site null-checks it.
