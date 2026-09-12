CREATE TABLE IF NOT EXISTS raw.olist_order_reviews (
    ingestion_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_file TEXT NOT NULL,
    record_hash TEXT NOT NULL,
    batch_id TEXT NOT NULL,

    review_id TEXT,
    order_id TEXT,
    review_score TEXT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TEXT,
    review_answer_timestamp TEXT,

    PRIMARY KEY (record_hash)
);

CREATE INDEX IF NOT EXISTS idx_olist_order_reviews_order_id
ON raw.olist_order_reviews (order_id);

CREATE INDEX IF NOT EXISTS idx_olist_order_reviews_review_id
ON raw.olist_order_reviews (review_id);