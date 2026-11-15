import psycopg2
from psycopg2.extensions import connection
from psycopg2 import OperationalError
from src.config import settings
from src.exceptions import BancoDeDadosError

def iniciar_conexao() -> connection:
    
    try:
        conexao = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME, 
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        return conexao

    except OperationalError as e:
        raise BancoDeDadosError(f"Falha de comunicação com o PostgreSQL: {e}")