from pathlib import Path
from itertools import islice
import pendulum
import uuid
import logging
from airflow.sdk import dag, task, get_current_context
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from src.extract.csv_loader import read_csv_with_metadata
from src.load.postgres_loader import load_to_postgres

@dag(
    dag_id="olist_raw_ingestion",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    default_args={
        "owner": "admin",
        "depends_on_past": False,
        "execution_timeout": pendulum.duration(minutes=10),
        "retries": 1,
    },
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["olist", "csv", "raw"],
)
def load_olist_raw_data():

    POSTGRES_CONN_ID = "postgres_olist_conn_id"

    @task
    def load_table_data(file: str, table: str):
        file_path = Path("/opt/airflow/datasets") / file
        run_id = get_current_context()["run_id"]
        log = logging.getLogger(run_id)

        records = read_csv_with_metadata(
            file_path=file_path,
            batch_id=run_id,
            ingestion_id=str(uuid.uuid5(uuid.NAMESPACE_URL, run_id)),
        )

        loaded = 0

        while batch := list(islice(records, 5000)):
            loaded += load_to_postgres(
                table_name=f"raw.{table}",
                records=batch,
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