CREATE TABLE IF NOT EXISTS raw.olist_sellers (
    ingestion_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_file TEXT NOT NULL,
    record_hash TEXT NOT NULL,
    batch_id TEXT NOT NULL,

    seller_id TEXT,
    seller_zip_code_prefix TEXT,
    seller_city TEXT,
    seller_state TEXT,

    PRIMARY KEY (record_hash)
);

CREATE INDEX IF NOT EXISTS idx_olist_sellers_seller_id
ON raw.olist_sellers (seller_id);