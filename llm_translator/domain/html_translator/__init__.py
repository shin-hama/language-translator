from pathlib import Path
from bs4 import BeautifulSoup

from domain.translator import Translator


class HtmlTranslator:
    def __init__(self, translator: Translator):
        self.translator = translator
        pass

    def translate(self, file: Path) -> str:
        with open(file, mode="r", encoding="utf-8-sig") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Step 1: 翻訳が必要なテキストとノードのペアを収集
        texts_to_translate = []
        nodes_to_translate = []

        for article in soup.find_all("article"):
            for node in article.find_all(text=True):
                if node.parent is None:
                    continue

                if node.parent.name in [
                    "script",
                    "style",
                    "[document]",
                    "code",
                    "h6",
                    "h5",
                    "h4",
                ]:
                    continue

                text = node.get_text(strip=True)
                if not text:
                    continue

                if not self._contains_japanese(text):
                    continue

                # 翻訳リストに追加
                texts_to_translate.append(text)
                nodes_to_translate.append(node)

        # Step 2: バッチで翻訳を実行
        if texts_to_translate:
            translated_texts = self.translator.translate(texts_to_translate)

            # Step 3: 翻訳結果でノードを置換
            for node, translated in zip(nodes_to_translate, translated_texts):
                node.replace_with(translated.strip().replace("\n", ""))

        return soup.prettify()

    def _contains_japanese(self, text: str) -> bool:
        for character in text:
            if (
                "\u3040" <= character <= "\u309f"
                or "\u30a0" <= character <= "\u30ff"
                or "\u4e00" <= character <= "\u9faf"
            ):
                return True
        return False
