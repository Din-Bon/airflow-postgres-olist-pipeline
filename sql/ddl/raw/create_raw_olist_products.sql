CREATE TABLE IF NOT EXISTS raw.olist_products (
    ingestion_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_file TEXT NOT NULL,
    record_hash TEXT NOT NULL,
    batch_id TEXT NOT NULL,

    product_id TEXT,
    product_category_name TEXT,
    product_name_lenght TEXT,
    product_description_lenght TEXT,
    product_photos_qty TEXT,
    product_weight_g TEXT,
    product_length_cm TEXT,
    product_height_cm TEXT,
    product_width_cm TEXT,

    PRIMARY KEY (record_hash)
);

CREATE INDEX IF NOT EXISTS idx_olist_products_product_id
ON raw.olist_products (product_id);