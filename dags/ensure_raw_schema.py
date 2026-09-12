import logging
from pathlib import Path
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from datetime import datetime, timedelta
from src.helper import load_sql, execute_sql

@dag(
    dag_id="ensure_raw_schema",
    start_date=datetime(2026, 1, 1,),
    default_args={
        "owner": "admin",
        "depends_on_past": False,
        "execution_timeout": timedelta(minutes=10),
        "retries": 1,
    },
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["olist", "csv", "raw"],
)
def ensure_raw_schema():

    POSTGRES_CONN_ID = "postgres_olist_conn_id"
    SQL_DIR = Path(__file__).parent.parent / "sql"

    @task
    def ensure_schema(sql_path: str):
        log = logging.getLogger(get_current_context()["ti"].dag_id)
        execute_sql(
            postgres_conn_id=POSTGRES_CONN_ID,
            sql_string=load_sql(sql_path).format(schema="raw"),
            log=log)
        log.info("Ensured raw schema")

    @task
    def ensure_table(sql_path: str, table_name: str):
        log = logging.getLogger(get_current_context()["ti"].dag_id)
        execute_sql(
            postgres_conn_id=POSTGRES_CONN_ID,
            sql_string=load_sql(sql_path),
            log=log)
        log.info(f"Ensured {table_name} table")

    ensure_schema(SQL_DIR / "ddl" / "create_schema.sql") >> [
            ensure_table(SQL_DIR / "ddl" / "raw" / "create_raw_olist_customers.sql", "Customers"),
            ensure_table(SQL_DIR / "ddl" / "raw" / "create_raw_olist_geolocation.sql", "Geolocation"),
            ensure_table(SQL_DIR / "ddl" / "raw" / "create_raw_olist_order_items.sql", "Order items"),
            ensure_table(SQL_DIR / "ddl" / "raw" / "create_raw_olist_order_payments.sql", "Payments"),
            ensure_table(SQL_DIR / "ddl" / "raw" / "create_raw_olist_order_reviews.sql", "Order reviews"),
            ensure_table(SQL_DIR / "ddl" / "raw" / "create_raw_olist_orders.sql", "Orders"),
            ensure_table(SQL_DIR / "ddl" / "raw" / "create_raw_olist_products.sql", "Products"),
            ensure_table(SQL_DIR / "ddl" / "raw" / "create_raw_olist_sellers.sql", "Sellers"),
            ensure_table(SQL_DIR / "ddl" / "raw" / "create_raw_product_category_name_translation.sql", "Product categories translation"),
        ]

ensure_raw_schema()