from logging import Logger
from pathlib import Path
from typing import Any, Dict, List
from src.helper import load_sql, execute_sql
from psycopg2 import sql

VALID_SCHEMAS = {
    "raw", "staging", "mart"
}

def load_to_postgres(
    table_name: str,
    records: List[Dict[str, Any]],
    postgres_conn_id: str,
    log: Logger = None,
) -> int:

    if not records:
        return 0

    schema, table = table_name.split(".")

    if schema not in VALID_SCHEMAS:
        raise ValueError(f"Invalid schema: {schema}")
    
    SQL_DIR = Path(__file__).parent.parent.parent / "sql" / "dml"
    columns = list(records[0].keys())
    values = [tuple(record[column] for column in columns) for record in records]

    sql_string = sql.SQL(load_sql(SQL_DIR / "insert_table.sql")).format(
        table_name=sql.Identifier(schema, table),
        columns=sql.SQL(", ").join(
            sql.Identifier(column) for column in columns
        )
    )

    placeholders = ", ".join(["%s"] * len(columns))
    execute_sql(postgres_conn_id, sql_string, values, template=f"({placeholders})", log=log)
    return len(values)
            