from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UsuarioResponse(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    cargo: str
    ativo: bool

    class Config:
        from_attributes = True


class MedicoCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    crm: str = Field(..., min_length=4)
    especialidade: Optional[str] = None
    email: EmailStr = Field(...)
    senha: str = Field(..., min_length=6)

class MedicoUpdate(BaseModel):
    nome: str = Field(..., min_length=3)
    crm: str = Field(..., min_length=4)
    especialidade: Optional[str] = None

class MedicoResponse(UsuarioResponse):
    nome: str
    crm: str
    especialidade: Optional[str] = None


class EnfermeiroCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    coren: str = Field(..., min_length=4)
    email: EmailStr = Field(...)
    senha: str = Field(..., min_length=6)

class EnfermeiroUpdate(BaseModel):
    nome: str = Field(..., min_length=3)
    coren: str = Field(..., min_length=4)

class EnfermeiroResponse(UsuarioResponse):
    nome: str
    coren: str


class CoordenadorCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    setor_responsavel: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(..., min_length=6)

class CoordenadorUpdate(BaseModel):
    nome: str = Field(..., min_length=3)
    setor_responsavel: str = Field(...)

class CoordenadorResponse(UsuarioResponse):
    nome: str
    setor_responsavel: str