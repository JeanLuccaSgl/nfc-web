CREATE TABLE establishments (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE qr_codes (
    id BIGSERIAL PRIMARY KEY,
    establishment_id BIGINT NOT NULL REFERENCES establishments(id),
    code TEXT NOT NULL UNIQUE,
    destination_url TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE access_events (
    id BIGSERIAL PRIMARY KEY,
    qr_code_id BIGINT NOT NULL REFERENCES qr_codes(id),
    accessed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_access_events_qr_code
ON access_events (qr_code_id);