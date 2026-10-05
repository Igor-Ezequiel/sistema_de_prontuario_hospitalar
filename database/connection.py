import psycopg2
from psycopg2.extensions import connection
from psycopg2 import OperationalError
from src.config import settings

def inciar_conexao() -> connection:
    
    try:
        conexao = psycopg2.connect(
            
            host = settings.DB_HOST,
            port = settings.DB_PORT,
            name = settings.DB_NAME,
            user = settings.DB_USER,
            password = settings.DB_PASSWORD
        )
        return conexao
        
    except OperationalError as e:
        
        print(f"Falha de comunicação com o PostgreSQL: {e}")
        raise e
        
        