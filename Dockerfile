FROM python:3.9-slim
COPY . ./korablinbot
WORKDIR ./korablinbot

RUN python -m pip install --upgrade pip && \
    apt-get update && \
    apt-get -y install libpq-dev gcc

RUN pip install poetry==1.1.12 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

RUN mkdir staticfiles