# Olist Medallion Pipeline

## Project overview

ETL-пайплайн для загрузки данных Brazilian E-Commerce Public Dataset (Olist) из CSV в PostgreSQL по медальон-архитектуре: raw(bronze) → staging(silver) → mart(gold).

## Architecture

```
    CSV --> Airflow
    Airflow --> Raw[(PostgreSQL raw)]
    Raw --> Staging[(PostgreSQL staging)]
    Staging --> Mart[(PostgreSQL mart)]
```

## Tech stack

- Python
- Apache Airflow
- PostgreSQL
- Docker Compose

## Repository structure

- `dags/` — DAG Airflow
- `src/` — Python-код (extract, transform, load)
- `sql/` — DDL и SQL-трансформации
- `datasets/` — инструкции по данным
- `docker/` — Dockerfile

## Quick start

```bash
# 1. Скопируй .env.example в .env
cp .env.example .env

# 2. Помести CSV-файлы Olist в директорию datasets/

# 3. Запусти окружение
docker compose up -d

# 4. Открой Airflow
http://localhost:8081

# 5. Запусти DAG olist_raw_ingestion
```

## Pipeline flow

1. DAG читает CSV из `datasets/`.
2. Добавляет системные поля.
3. Загружает в `raw.olist_*`.
4. Нормализация в `staging.*`.
5. Витрины в `mart.*`.

## Data model

### Raw

Каждая raw-таблица содержит:

- `ingestion_id`
- `ingested_at`
- `source_file`
- `record_hash`
- `batch_id`
- бизнес-поля

## Development

## Roadmap

- [x] Repository structure
- [x] Docker Compose
- [x] Basic CSV ingestion to raw
- [ ] Staging transformations
- [ ] Star schema marts
- [ ] Incremental loads
- [ ] Data quality checks
- [ ] CI