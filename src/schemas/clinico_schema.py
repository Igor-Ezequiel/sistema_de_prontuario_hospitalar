from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CIDResponse(BaseModel):
    codigo: str
    descricao: str

    class Config:
        from_attributes = True


class TriagemCreate(BaseModel):
    pressao: str = Field(..., description="Ex: 12/8")
    temperatura: float = Field(...)
    saturacao: int = Field(...)
    atendimento_id: int
    enfermeiro_id: int

class TriagemResponse(BaseModel):
    id: int
    pressao: str
    temperatura: float
    saturacao: int
    data_hora: datetime
    atendimento_id: Optional[int]
    enfermeiro_id: Optional[int]

    class Config:
        from_attributes = True


class PrescricaoCreate(BaseModel):
    nome_medicamento: str = Field(...)
    dose: str = Field(...)
    intervalo_horas: int = Field(...)
    evolucao_id: int = Field(...)

class PrescricaoResponse(BaseModel):
    id: int
    nome_medicamento: str
    dose: str
    intervalo_horas: int
    status: str
    evolucao_id: Optional[int]
    enfermeiro_id: Optional[int] = None
    data_hora_aplicacao: Optional[datetime] = None

    class Config:
        from_attributes = True


class EvolucaoCreate(BaseModel):
    relato: str = Field(..., min_length=10)
    dias_entubacao: Optional[int] = None
    atendimento_id: int
    medico_id: int
    lista_cids: Optional[List[str]] = []

class EvolucaoUpdate(BaseModel):
    relato: str = Field(..., min_length=10)
    dias_entubacao: Optional[int] = None
    medico_id: int 

class EvolucaoResponse(BaseModel):
    id: int
    relato: str
    dias_entubacao: Optional[int]
    data_hora: datetime
    atendimento_id: Optional[int]
    medico_id: Optional[int]
    medico_autor: Optional[str] = None
    
   
    diagnosticos: List[CIDResponse] = []
    prescricoes: List[PrescricaoResponse] = []

    class Config:
        from_attributes = True