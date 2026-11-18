from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ==========================================
# USUÁRIO E LOGIN (UsuarioService)
# ==========================================
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str = Field(..., min_length=6)
    cargo: str
    ativo: Optional[bool] = True

class UsuarioCredenciaisUpdate(BaseModel):
    email: EmailStr
    senha: Optional[str] = Field(None, min_length=6)

class UsuarioResponse(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    cargo: str
    ativo: bool

    class Config:
        from_attributes = True

# ==========================================
# MÉDICO (MedicoService)
# ==========================================
class MedicoCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    crm: str = Field(..., min_length=4)
    especialidade: str = Field(...)
    email: EmailStr
    senha: str = Field(..., min_length=6)

class MedicoUpdate(BaseModel):
    nome: str = Field(..., min_length=3)
    crm: str = Field(..., min_length=4)
    especialidade: str = Field(...)

class MedicoResponse(UsuarioResponse):
    nome: str
    crm: str
    especialidade: Optional[str] = None

# ==========================================
# ENFERMEIRO (EnfermeiroService)
# ==========================================
class EnfermeiroCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    coren: str = Field(..., min_length=4)
    email: EmailStr
    senha: str = Field(..., min_length=6)

class EnfermeiroUpdate(BaseModel):
    nome: str = Field(..., min_length=3)
    coren: str = Field(..., min_length=4)

class EnfermeiroResponse(UsuarioResponse):
    nome: str
    coren: str

# ==========================================
# COORDENADOR (CoordenadorService)
# ==========================================
class CoordenadorCreate(BaseModel):
    nome: str = Field(..., min_length=3)
    setor_responsavel: str = Field(...)
    email: EmailStr
    senha: str = Field(..., min_length=6)

class CoordenadorUpdate(BaseModel):
    nome: str = Field(..., min_length=3)
    setor_responsavel: str = Field(...)

class CoordenadorResponse(UsuarioResponse):
    nome: str
    setor_responsavel: str