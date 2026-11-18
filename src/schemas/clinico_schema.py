from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from src.models.Classes import CorRisco
from src.schemas.equipe_schema import EnfermeiroResponse

# ==========================================
# CID
# ==========================================
class CIDResponse(BaseModel):
    codigo: str
    descricao: str

    class Config:
        from_attributes = True

# ==========================================
# TRIAGEM (TriagemService)
# ==========================================
class TriagemCreate(BaseModel):
    # Espelha o seu Criar_triagem (que exige a nova_cor!)
    atendimento_id: int
    enfermeiro_id: int
    pressao: str = Field(..., description="Ex: 12/8")
    temperatura: float
    saturacao: int
    nova_cor: CorRisco

class TriagemUpdate(BaseModel):
    # Espelha o seu atualizar_triagem
    nova_pressao: str
    nova_temperatura: float
    nova_saturacao: int

class TriagemResponse(BaseModel):
    id: int
    pressao: str
    temperatura: float
    saturacao: int
    data_hora: Optional[datetime] = None
    atendimento_id: Optional[int] = None
    enfermeiro_id: Optional[int] = None
    enfermeiro: Optional[EnfermeiroResponse] = None

    class Config:
        from_attributes = True

# ==========================================
# PRESCRIÇÃO (PrescricaoService)
# ==========================================
class PrescricaoCreate(BaseModel):
    nome_medicamento: str = Field(...)
    dose: str = Field(...)
    intervalo_horas: int = Field(...)
    evolucao_id: int

class PrescricaoAplicar(BaseModel):
    # Usado pelo enfermeiro no aplicar_medicamento
    enfermeiro_id: int

class PrescricaoResponse(BaseModel):
    id: int
    nome_medicamento: str
    dose: str
    intervalo_horas: int
    status: str
    evolucao_id: Optional[int] = None
    enfermeiro_id: Optional[int] = None
    data_hora_aplicacao: Optional[datetime] = None
    enfermeiro: Optional[EnfermeiroResponse] = None

    class Config:
        from_attributes = True

# ==========================================
# EVOLUÇÃO (EvolucaoService)
# ==========================================
class EvolucaoCreate(BaseModel):
    atendimento_id: int
    medico_id: int
    relato: str = Field(..., min_length=1)
    dias_entubacao: Optional[int] = 0
    lista_cids: Optional[List[str]] = None

class EvolucaoUpdate(BaseModel):
    medico_id: int
    novo_relato: str = Field(..., min_length=1)
    novos_dias_entubacao: Optional[int] = None

class DiagnosticoVincular(BaseModel):
    # Espelha o seu vincular_novo_diagnostico
    medico_id: int
    codigo_cid: str

class EvolucaoResponse(BaseModel):
    id: int
    relato: str
    dias_entubacao: Optional[int] = None
    data_hora: datetime
    atendimento_id: Optional[int] = None
    medico_id: Optional[int] = None
    medico_autor: Optional[str] = None
    
    diagnosticos: List[CIDResponse] = []
    prescricoes: List[PrescricaoResponse] = []

    class Config:
        from_attributes = True