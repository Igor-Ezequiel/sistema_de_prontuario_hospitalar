from fastapi import HTTPException, status
from database.connection import iniciar_conexao 
from src.exceptions import BancoDeDadosError

def get_db():
    conexao = None
    try:
        conexao = iniciar_conexao()
       
        yield conexao
    except BancoDeDadosError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
       
        if conexao:
            conexao.close()