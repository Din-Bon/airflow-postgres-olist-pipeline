CREATE TABLE IF NOT EXISTS raw.olist_geolocation (
    ingestion_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_file TEXT NOT NULL,
    record_hash TEXT NOT NULL,
    batch_id TEXT NOT NULL,

    geolocation_zip_code_prefix TEXT,
    geolocation_lat TEXT,
    geolocation_lng TEXT,
    geolocation_city TEXT,
    geolocation_state TEXT,

    PRIMARY KEY (record_hash)
);