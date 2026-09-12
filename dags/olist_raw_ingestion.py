from datetime import datetime, timedelta
from pathlib import Path
import uuid
import logging
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from src.extract.csv_loader import read_csv_with_metadata
from src.load.postgres_loader import load_to_postgres

@dag(
    dag_id="olist_raw_ingestion",
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
    tags=["api", "json"],
)
def load_olist_raw_data():

    POSTGRES_CONN_ID = "postgres_olist_conn_id"
    INGESTION_ID = str(uuid.uuid4())

    @task
    def load_table_data(file: str, table: str):
        file_path = Path("/opt/airflow/datasets") / file
        ti = get_current_context()["ti"]
        log = logging.getLogger(ti.dag_id)

        records = list(
            read_csv_with_metadata(
                file_path=file_path,
                batch_id=ti.dag_id,
                ingestion_id=INGESTION_ID,
            )
        )

        loaded = load_to_postgres(
            table_name=f"raw.{table}",
            records=records,
            postgres_conn_id=POSTGRES_CONN_ID,
            log=log,
        )

        log.info(f"Loaded {loaded} records into raw.{table}")

    TriggerDagRunOperator(
        task_id="ensure_raw_schema",
        trigger_dag_id="ensure_raw_schema",
        wait_for_completion=True,
        poke_interval=5,
    ) >> [
        load_table_data("olist_customers_dataset.csv", "olist_customers"),
        load_table_data("olist_geolocation_dataset.csv", "olist_geolocation"),
        load_table_data("olist_order_items_dataset.csv", "olist_order_items"),
        load_table_data("olist_order_payments_dataset.csv", "olist_order_payments"),
        load_table_data("olist_order_reviews_dataset.csv", "olist_order_reviews"),
        load_table_data("olist_orders_dataset.csv", "olist_orders"),
        load_table_data("olist_products_dataset.csv", "olist_products"),
        load_table_data("olist_sellers_dataset.csv", "olist_sellers"),
        load_table_data("product_category_name_translation.csv", "product_category_name_translation"),
    ]

load_olist_raw_data()