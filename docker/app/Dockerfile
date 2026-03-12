FROM python:3.14-slim

ENV PYTHONPATH=/src/src/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock /src/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY ./alembic.ini /src/alembic.ini
COPY ./alembic /src/alembic
COPY ./src /src/src
