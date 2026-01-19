FROM python:3.11-slim

WORKDIR /app

RUN apt-get update &&\
    apt-get -y install locales git curl &&\
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN pip install --upgrade pip

# uvのインストール
RUN pip install uv

COPY ./pyproject.toml ./uv.lock* ./

RUN uv sync --frozen

COPY ./llm_translator/ ./llm_translator
