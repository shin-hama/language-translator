# 翻訳システム

LLM を使ったテキスト翻訳システム。
機密情報を翻訳するためにローカルで動作する翻訳システムが必要となったので作成した。

## Getting Started

上から順番に簡単なやり方

### docker

1. 以下コマンドを実行

    ```shell
    docker compose up -d
    ```

2. 以下コマンドでコンテナに入って実行

    ```shell
    docker exec -it bash llm-translator
    ```

### poetry を利用

1. 以下コマンドを実行

    ```shell
    poetry install
    ```

2. 仮想環境を起動して実行

### requirements.txt を利用

1. 仮想環境を作成
2. 以下コマンドを実行して依存関係をインストール

    ```shell
    pip install -r requirements.txt
    ```

3. 仮想環境を起動して実行
