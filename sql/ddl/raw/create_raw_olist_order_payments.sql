CREATE TABLE IF NOT EXISTS raw.olist_order_payments (
    ingestion_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_file TEXT NOT NULL,
    record_hash TEXT NOT NULL,
    batch_id TEXT NOT NULL,

    order_id TEXT,
    payment_sequential TEXT,
    payment_type TEXT,
    payment_installments TEXT,
    payment_value TEXT,

    PRIMARY KEY (record_hash)
);

CREATE INDEX IF NOT EXISTS idx_olist_order_payments_order_id
ON raw.olist_order_payments (order_id);