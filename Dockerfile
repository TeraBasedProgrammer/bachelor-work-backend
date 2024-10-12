FROM python:3.10.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-root

COPY ./poetry.lock ./pyproject.toml /app/

COPY . /app

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]