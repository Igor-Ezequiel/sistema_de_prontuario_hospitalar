from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PacienteCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    cpf: str = Field(..., min_length=11, max_length=14)
    data_nascimento: date = Field(...)
    usuario_id: Optional[int] = None

class PacienteUpdate(BaseModel):
    nome: str = Field(..., min_length=3)
    data_nascimento: date
    ativo: bool

class PacienteResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    data_nascimento: date
    ativo: bool
    usuario_id: Optional[int] = None

    class Config:
        from_attributes = True