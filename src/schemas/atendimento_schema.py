from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from src.models.Classes import StatusAtendimento, CorRisco

from src.schemas.clinico_schema import TriagemResponse, EvolucaoResponse


class PlantaoCreate(BaseModel):
    setor_ala: str
    data_hora_inicio: datetime
    data_hora_fim: datetime
    medico_id: int
    coordenador_id: int

class PlantaoResponse(BaseModel):
    id: int
    setor_ala: str
    data_hora_inicio: datetime
    data_hora_fim: datetime
    medico_id: int
    coordenador_id: int

    class Config:
        from_attributes = True


class AtendimentoCreate(BaseModel):
    paciente_id: int
    cor_risco: CorRisco

class AtendimentoUpdate(BaseModel):
    status: StatusAtendimento
    cor_risco: CorRisco
    medico_id: Optional[int] = None

class AtendimentoResponse(BaseModel):
    id: int
    status: StatusAtendimento
    cor_risco: CorRisco
    data_entrada: datetime
    data_alta: Optional[datetime] = None
    paciente_id: int
    medico_id: Optional[int] = None
    
    triagens: List[TriagemResponse] = []
    evolucoes: List[EvolucaoResponse] = []
    
    class Config:
        from_attributes = True