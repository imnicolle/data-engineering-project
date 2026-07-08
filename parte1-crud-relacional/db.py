"""
Conexão com o banco PostgreSQL hospedado no AWS RDS.
Configure as credenciais via variáveis de ambiente (recomendado) ou
edite os valores padrão abaixo.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "SEU_ENDPOINT.rds.amazonaws.com"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "trabalho_ed"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "SUA_SENHA"),
}


def get_connection():
    """Abre e retorna uma nova conexão com o banco."""
    return psycopg2.connect(cursor_factory=RealDictCursor, **DB_CONFIG)
