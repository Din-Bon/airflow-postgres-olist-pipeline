import csv
import hashlib
from pathlib import Path
from typing import Iterator


def compute_record_hash(row: dict) -> str:
    row_str = "|".join(f"{k}={v}" for k, v in sorted(row.items()))
    return hashlib.sha256(row_str.encode("utf-8-sig")).hexdigest()


def read_csv_with_metadata(
    file_path: Path,
    batch_id: str,
    ingestion_id: str,
) -> Iterator[dict]:
    with file_path.open("r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        source_file = str(file_path)

        for row in reader:
            row["record_hash"] = compute_record_hash(row)
            row["ingestion_id"] = ingestion_id
            row["source_file"] = source_file
            row["batch_id"] = batch_id
            yield row