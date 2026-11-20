from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.schemas.clinico_schema import (
    EvolucaoCreate,
    EvolucaoUpdate,
    DiagnosticoVincular,
    EvolucaoResponse,
    CIDResponse
)
from src.repositori.EvolucaoRepository import EvolucaoRepository
from src.repositori.AtendimentoRepository import AtendimentoRepository
from src.repositori.CID_Repository import CIDRepository
from src.service.EvolucaoService import EvolucaoService
from src.exceptions import NaoEncontradoError, RegraDeNegocioError, PermissaoNegadaError
from src.deps import get_db

router = APIRouter(prefix="/evolucoes", tags=["Clínico - Evoluções"])

def obter_service(db) -> EvolucaoService:
    return EvolucaoService(
        evolucao_repo=EvolucaoRepository(db),
        atendimento_repo=AtendimentoRepository(db),
        cid_repo=CIDRepository(db)
    )

@router.post("/", response_model=EvolucaoResponse, status_code=status.HTTP_201_CREATED)
def registrar_nova_evolucao(dados: EvolucaoCreate, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.registrar_nova_evolucao(
            atendimento_id=dados.atendimento_id,
            medico_id=dados.medico_id,
            relato=dados.relato,
            dias_entubacao=dados.dias_entubacao,
            lista_cids=dados.lista_cids
        )
    except PermissaoNegadaError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{id_evolucao}/diagnosticos", response_model=CIDResponse, status_code=status.HTTP_201_CREATED)
def vincular_novo_diagnostico(id_evolucao: int, dados: DiagnosticoVincular, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.vincular_novo_diagnostico(
            id_evolucao=id_evolucao,
            medico_id=dados.medico_id,
            codigo_cid=dados.codigo_cid
        )
    except PermissaoNegadaError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_evolucao}", response_model=EvolucaoResponse)
def buscar_evolucao_por_id(id_evolucao: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_evolucao_por_id(id_evolucao)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/atendimento/{atendimento_id}", response_model=List[EvolucaoResponse])
def buscar_historico_por_atendimento(atendimento_id: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_historico_por_atendimento(atendimento_id)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{id_evolucao}", response_model=EvolucaoResponse)
def atualizar_evolucao(id_evolucao: int, dados: EvolucaoUpdate, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.atualizar_evolucao(
            id_evolucao=id_evolucao,
            medico_id=dados.medico_id,
            novo_relato=dados.novo_relato,
            novos_dias_entubacao=dados.novos_dias_entubacao
        )
    except PermissaoNegadaError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id_evolucao}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evolucao(id_evolucao: int, medico_id: int, db = Depends(get_db)):
    """Recebe medico_id via Query Param (ex: DELETE /evolucoes/5?medico_id=2)"""
    try:
        service = obter_service(db)
        service.excluir_evolucao(id_evolucao, medico_id)
        return None
    except PermissaoNegadaError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))