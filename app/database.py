import psycopg # Biblioteca para conexão com o banco de dados PostgreSQL

from app.config import DATABASE_URL # Busca a URL de conexão no arquivo de configuração


def abrir_conexao(): #Abre a conexão com o banco de dados
    return psycopg.connect(DATABASE_URL)