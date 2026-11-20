from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from src.config import settings
from src.exceptions import BancoDeDadosError


class SessaoSQL(Session):
    def execute(self, statement, *args, **kwargs):
        if isinstance(statement, str):
            statement = text(statement)
        return super().execute(statement, *args, **kwargs)


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=SessaoSQL,
)


def iniciar_conexao() -> Session:
    try:
        return SessionLocal()
    except OperationalError as e:
        raise BancoDeDadosError(f"Falha de comunicação com o PostgreSQL: {e}")