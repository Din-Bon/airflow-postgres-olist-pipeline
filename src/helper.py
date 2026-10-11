from psycopg2.extras import execute_values
from logging import Logger
from pathlib import Path
from airflow.providers.postgres.hooks.postgres import PostgresHook

def load_sql(path_str: str) -> str:
    path = Path(path_str)

    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {path}")
    
    return path.read_text(encoding="utf-8-sig").strip()

def execute_sql(
        postgres_conn_id: str,
        sql_string: str,
        parameters: list = None,
        page_size: int = 1000,
        template: str = None,
        log: Logger = None):
    with PostgresHook(postgres_conn_id=postgres_conn_id).get_conn() as conn:
        with conn.cursor() as cursor:
            try:
                if parameters:
                    execute_values(cur=cursor, sql=sql_string, argslist=parameters, template=template, page_size=page_size)
                else:
                    cursor.execute(sql_string)
                conn.commit()
            except Exception as ex:
                if log != None:
                    log.error(f"SQL command failed: \n{sql_string}\n\n{ex}")

                conn.rollback()
                raise