FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install poetry poetry-plugin-export

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    poetry export --format requirements.txt --output requirements_test.txt --without-hashes --only dev

FROM python:3.12-slim AS app

WORKDIR /usr/src/app

COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_test.txt

COPY . .

CMD python cli.py sleep
