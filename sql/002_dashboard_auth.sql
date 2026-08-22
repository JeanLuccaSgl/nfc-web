-- Vínculo entre uma conta do Supabase Auth e o estabelecimento que ela pode acessar.
ALTER TABLE establishments
ADD COLUMN IF NOT EXISTS dashboard_user_id UUID
REFERENCES auth.users(id)
ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_establishments_dashboard_user_id
ON establishments (dashboard_user_id);

-- Mantém o histórico antigo compatível e registra a origem dos novos acessos.
ALTER TABLE access_events
ADD COLUMN IF NOT EXISTS source TEXT NOT NULL DEFAULT 'qr';

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'access_events_source_check'
    ) THEN
        ALTER TABLE access_events
        ADD CONSTRAINT access_events_source_check
        CHECK (source IN ('qr', 'nfc'));
    END IF;
END $$;
