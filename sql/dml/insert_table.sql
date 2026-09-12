INSERT INTO {table_name} ({columns})
VALUES %s
ON CONFLICT (record_hash) DO NOTHING