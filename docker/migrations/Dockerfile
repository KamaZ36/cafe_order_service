FROM python:3.14-slim

ENV PYTHONPATH=/src/src/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

RUN pip install --upgrade pip

RUN pip install python-dotenv
RUN pip install alembic
RUN pip install asyncpg

COPY ./alembic.ini /src/alembic.ini
COPY ./alembic /src/alembic
COPY ./src /src/src