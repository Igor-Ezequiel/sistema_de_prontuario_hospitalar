from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
from src.models.Classes import StatusAtendimento, CorRisco
from src.schemas.clinico_schema import TriagemResponse, EvolucaoResponse
from src.schemas.paciente_schema import PacienteResponse
from src.schemas.equipe_schema import MedicoResponse, CoordenadorResponse

# ==========================================
# PLANTÃO (PlantaoService)
# ==========================================
class PlantaoCreate(BaseModel):
    coordenador_id: int
    medico_id: int
    setor_ala: str
    data_hora_inicio: datetime
    data_hora_fim: datetime

class PlantaoUpdate(BaseModel):
    coordenador_id: int
    medico_id: int
    setor_ala: str
    data_hora_inicio: datetime
    data_hora_fim: datetime

class PlantaoResponse(BaseModel):
    id: int
    setor_ala: str
    data_hora_inicio: datetime
    data_hora_fim: datetime
    medico_id: int
    coordenador_id: int
    medico: Optional[MedicoResponse] = None
    coordenador: Optional[CoordenadorResponse] = None

    class Config:
        from_attributes = True

# ==========================================
# ATENDIMENTO E FILA (AtendimentoService)
# ==========================================
class AtendimentoCreate(BaseModel):
    # Espelha criar_atendimento(self, paciente_id: int)
    paciente_id: int

class ClassificarRiscoRequest(BaseModel):
    # Espelha Classificar_Risco(self, atendimento_id: int, nova_cor: CorRisco)
    nova_cor: CorRisco

class DarAltaRequest(BaseModel):
    # Espelha dar_alta(self, atendimento_id: int, medico_id: int)
    medico_id: int

class ChamarPacienteRequest(BaseModel):
    # Espelha Chamar_Paciente(self, medico_id: int)
    medico_id: int

class PermissaoExtraRequest(BaseModel):
    # Espelha conceder_permissao_extra(self, atendimento_id, coordenador_id, medico_id, motivo)
    coordenador_id: int
    medico_id: int
    motivo: str = Field(..., min_length=3)

class AtendimentoResponse(BaseModel):
    id: int
    status: StatusAtendimento
    cor_risco: CorRisco
    data_entrada: datetime
    data_alta: Optional[datetime] = None
    paciente_id: int
    medico_id: Optional[int] = None
    
    paciente: Optional[PacienteResponse] = None
    medico: Optional[MedicoResponse] = None
    triagens: List[TriagemResponse] = []
    evolucoes: List[EvolucaoResponse] = []
    permissoes_extras: List[Any] = []

    class Config:
        from_attributes = True