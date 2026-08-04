import psycopg2
from psycopg2.extras import RealDictCursor
from backend.config import settings

def get_db_connection():
    """
    Retorna uma conexão ativa com o banco PostgreSQL.
    Retorna None caso ocorra erro (permitindo fallback no backend).
    """
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASS,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Alerta: Não foi possível conectar ao banco ({e}).")
        return None
