FROM python:3.10-slim-buster

ARG POETRY_VERSION=1.1.12

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV HASH_FUNCTION=bcrypt
ENV SECRET_KEY=skdfhakjsfhakljfdhalkjfh8736483248372648372hjkdhfakjlhdsfjka
ENV ALGORITHM=HS256
ENV DB_URL=postgres://postgres:postgres@db:5432/codeshare

RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

COPY . /app/
RUN poetry install --no-interaction --no-ansi