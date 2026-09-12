CREATE TABLE IF NOT EXISTS raw.product_category_name_translation (
    ingestion_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_file TEXT NOT NULL,
    record_hash TEXT NOT NULL,
    batch_id TEXT NOT NULL,

    product_category_name TEXT,
    product_category_name_english TEXT,

    PRIMARY KEY (record_hash)
);

CREATE INDEX IF NOT EXISTS idx_product_category_name_translation_product_category_name
ON raw.product_category_name_translation (product_category_name);