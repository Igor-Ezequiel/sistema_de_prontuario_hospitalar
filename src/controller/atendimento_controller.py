from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.atendimento_schema import (
    AtendimentoCreate,
    ClassificarRiscoRequest,
    DarAltaRequest,
    ChamarPacienteRequest,
    PermissaoExtraRequest,
    AtendimentoResponse
)
from src.repositori.AtendimentoRepository import AtendimentoRepository
from repositori.Equipe_Medica.MedicoRepository import MedicoRepositori
from repositori.PlantaoRepository import PlantaoRepositori
from repositori.PermissaoExtraRepository import PermissaoExtraRepositori
from src.service.AtendimentoService import AtendimentoService
from src.service.SistemaFilaPrioridade import fila_hospital
from src.exceptions import NaoEncontradoError, RegraDeNegocioError, PermissaoNegadaError
from src.deps import get_db

router = APIRouter(prefix="/atendimentos", tags=["Recepção e Fluxo de Atendimento"])

def obter_service(db) -> AtendimentoService:
    return AtendimentoService(
        repositori=AtendimentoRepository(db),
        repositori_medico=MedicoRepositori(db),
        repositori_plantao=PlantaoRepositori(db),
        repositori_permissao_extra=PermissaoExtraRepositori(db)
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_atendimento(dados: AtendimentoCreate, db = Depends(get_db)):
    try:
        service = obter_service(db)
        id_gerado = service.criar_atendimento(dados.paciente_id)
        return {"mensagem": "Atendimento iniciado (Aguardando Triagem)", "id": id_gerado}
    except (RegraDeNegocioError, NaoEncontradoError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.get("/fila/status")
def consultar_status_fila():
    """Exibe informações em tempo real do SistemaFilaPrioridade"""
    return {
        "pacientes_aguardando": fila_hospital.Verificar_Tamanho(),
        "fila_vazia": fila_hospital.Verificar_Estado_Fila(),
        "capacidade_maxima_atingida": fila_hospital.Verificar_QuantidadeMax()
    }

@router.post("/chamar-proximo", response_model=AtendimentoResponse)
def chamar_proximo_paciente(dados: ChamarPacienteRequest, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.Chamar_Paciente(dados.medico_id)
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{atendimento_id}", response_model=AtendimentoResponse)
def buscar_atendimento_simples(atendimento_id: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_atendimento(atendimento_id)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{atendimento_id}/prontuario", response_model=AtendimentoResponse)
def buscar_prontuario_completo(atendimento_id: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_prontuario(atendimento_id)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{atendimento_id}/auditoria", response_model=AtendimentoResponse)
def buscar_prontuario_auditoria(atendimento_id: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_prontuario_para_auditoria(atendimento_id)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{atendimento_id}/risco")
def classificar_risco_emergencia(atendimento_id: int, dados: ClassificarRiscoRequest, db = Depends(get_db)):
    try:
        service = obter_service(db)
        service.Classificar_Risco(atendimento_id, dados.nova_cor)
        return {"mensagem": f"Risco reclassificado para {dados.nova_cor.value}"}
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{atendimento_id}/alta")
def dar_alta_paciente(atendimento_id: int, dados: DarAltaRequest, db = Depends(get_db)):
    try:
        service = obter_service(db)
        service.dar_alta(atendimento_id, dados.medico_id)
        return {"mensagem": "Alta médica registrada com sucesso"}
    except PermissaoNegadaError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{atendimento_id}/permissao-extra", response_model=AtendimentoResponse)
def conceder_permissao_extra(atendimento_id: int, dados: PermissaoExtraRequest, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.conceder_permissao_extra(
            atendimento_id=atendimento_id,
            coordenador_id=dados.coordenador_id,
            medico_id=dados.medico_id,
            motivo=dados.motivo
        )
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{atendimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_atendimento(atendimento_id: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        service.Deletar_Atendimento(atendimento_id)
        return None
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))