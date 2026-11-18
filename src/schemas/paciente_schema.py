from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from src.schemas.equipe_schema import UsuarioResponse

class PacienteCreate(BaseModel):
    # No seu PacienteService.cadastrar_paciente, só entram esses 3 campos
    # (o usuario_id você mesmo descobre buscando pelo CPF lá dentro!)
    nome: str = Field(..., min_length=3)
    cpf: str = Field(..., min_length=11, max_length=14)
    data_nascimento: date

class PacienteUpdate(BaseModel):
    # Espelha o seu PacienteService.atualizar_dados
    nome: str = Field(..., min_length=3)
    cpf: str = Field(..., min_length=11, max_length=14)
    data_nascimento: date
    usuario_id: Optional[int] = None

class PacienteResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    data_nascimento: date
    ativo: bool
    usuario_id: Optional[int] = None
    usuario: Optional[UsuarioResponse] = None

    class Config:
        from_attributes = True