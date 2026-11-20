from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database.connection import SessionLocal
from src.exceptions import BancoDeDadosError


def get_db():
    db = SessionLocal()
    try:
        yield db
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registo duplicado ou violação de integridade (e-mail, CPF ou CRM já registado).",
        )
    except (SQLAlchemyError, BancoDeDadosError):
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar operação na base de dados.",
        )
    finally:
        db.close()