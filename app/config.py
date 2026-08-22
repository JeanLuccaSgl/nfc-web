import os

DATABASE_URL = os.environ["DATABASE_URL"]
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_PUBLISHABLE_KEY = os.environ.get("SUPABASE_PUBLISHABLE_KEY", "")
CORS_ORIGINS = [
    origem.strip()
    for origem in os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origem.strip()
]
