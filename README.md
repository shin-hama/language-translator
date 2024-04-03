# 翻訳システム

LLM を使ったテキスト翻訳システム。
機密情報を翻訳するためにローカルで動作する翻訳システムが必要となったので作成した。

## Getting Started

### パッケージをインストール

#### GitHub からインストール

1. [リリースページ](https://github.com/shamada4151/llm-translator/releases)からパッケージファイルをダウンロードしてインストール

    ```shell
    pip install llm_translator-0.1.0-py3-none-any.whl
    ```

#### PyPI からインストール

Azure の [jeol-em-1g](https://jeol-em-1g.visualstudio.com/) にアクセスできる人はこちらも可能

1. PAT を作成
   1. 権限は Packaging の Read のみで良い
2. 以下コマンドを実行
   1. 尋ねられたら User と PAT を入力する

    ```shell
    pip install llm-translator --index-url https://jeol-em-1g.pkgs.visualstudio.com/Donau/_packaging/JEOL-PyPI/pypi/simple/
    ```

### ソースコードから実行

<https://github.com/shamada4151/llm-translator> からソースコードを取得して以下の手順で実行

### docker

1. 以下コマンドを実行

    ```shell
    docker compose up -d
    ```

2. 以下コマンドでコンテナに入って実行

    ```shell
    docker exec -it bash llm-translator
    python -m llm_translator --version
    ```

### poetry を利用

1. 以下コマンドを実行

    ```shell
    poetry install
    ```

2. 仮想環境を起動して実行

    ```shell
    poetry shell
    python -m llm_translator --version
    ```

### requirements.txt を利用

1. 仮想環境を作成
2. 以下コマンドを実行して依存関係をインストール

    ```shell
    pip install -r requirements.txt
    pip install -e .
    ```

3. 仮想環境を起動して実行

    ```shell
    .venv/Scripts/python -m llm_translator --version
    ```
