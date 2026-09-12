from logging import Logger
from pathlib import Path
from typing import Any, Dict, List
from src.helper import load_sql, execute_sql


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

    schema, _ = table_name.split(".")

    if schema not in VALID_SCHEMAS:
        raise ValueError(f"Invalid schema: {schema}")

    SQL_DIR = Path(__file__).parent.parent.parent / "sql" / "dml"
    columns = list(records[0].keys())
    values = [tuple(record[column] for column in columns) for record in records]

    sql = load_sql(SQL_DIR / "insert_table.sql").format(
        table_name=table_name,
        columns=", ".join(columns),
    )

    placeholders = ", ".join(["%s"] * len(columns))
    execute_sql(postgres_conn_id, sql, values, template=f"({placeholders})", log=log)
    return len(values)
            