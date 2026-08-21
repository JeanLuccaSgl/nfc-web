import psycopg

from app.config import DATABASE_URL


def abrir_conexao():
    return psycopg.connect(DATABASE_URL)