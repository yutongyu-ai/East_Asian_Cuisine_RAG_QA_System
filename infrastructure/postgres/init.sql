CREATE TABLE IF NOT EXISTS message_store (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_session_id ON message_store(session_id);