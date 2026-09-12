CREATE TABLE IF NOT EXISTS raw.olist_customers (
    ingestion_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_file TEXT NOT NULL,
    record_hash TEXT NOT NULL,
    batch_id TEXT NOT NULL,

    customer_id TEXT NOT NULL,
    customer_unique_id TEXT NOT NULL,
    customer_zip_code_prefix TEXT,
    customer_city TEXT,
    customer_state TEXT,

    PRIMARY KEY (record_hash)
);

CREATE INDEX IF NOT EXISTS idx_olist_customers_customer_id
ON raw.olist_customers (customer_id);