FROM python:3.9-slim-buster

ARG POETRY_VERSION=1.1.12

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV HASH_FUNCTION=bcrypt
ENV SECRET_KEY=skdfhakjsfhakljfdhalkjfh8736483248372648372hjkdhfakjlhdsfjka
ENV ALGORITHM=HS256

RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

COPY . /app/
RUN poetry install --no-interaction --no-ansi
RUN mkdir data
RUN python3 manage.py create_tables
RUN apt update && apt upgrade && apt install sqlite3
