from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.schemas.clinico_schema import TriagemCreate, TriagemUpdate, TriagemResponse
from src.repositori.TriagemRepository import TriagemRepository
from src.repositori.AtendimentoRepository import AtendimentoRepository
from src.service.TriagemService import TriagemService
from src.exceptions import NaoEncontradoError, RegraDeNegocioError
from src.deps import get_db

router = APIRouter(prefix="/triagens", tags=["Clínico - Triagem"])

def obter_service(db) -> TriagemService:
    return TriagemService(TriagemRepository(db), AtendimentoRepository(db))

@router.post("/", response_model=TriagemResponse, status_code=status.HTTP_201_CREATED)
def criar_triagem(dados: TriagemCreate, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.Criar_triagem(
            atendimento_id=dados.atendimento_id,
            enfermeiro_id=dados.enfermeiro_id,
            pressao=dados.pressao,
            temperatura=dados.temperatura,
            saturacao=dados.saturacao,
            nova_cor=dados.nova_cor
        )
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_triagem}", response_model=TriagemResponse)
def buscar_triagem_por_id(id_triagem: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_triagem_por_id(id_triagem)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/atendimento/{atendimento_id}", response_model=List[TriagemResponse])
def buscar_historico_triagens(atendimento_id: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_historico(atendimento_id)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{triagem_id}")
def atualizar_triagem(triagem_id: int, dados: TriagemUpdate, db = Depends(get_db)):
    try:
        service = obter_service(db)
        service.atualizar_triagem(
            triagem_id=triagem_id,
            nova_pressao=dados.nova_pressao,
            nova_temperatura=dados.nova_temperatura,
            nova_saturacao=dados.nova_saturacao
        )
        return {"mensagem": "Dados da triagem atualizados com sucesso"}
    except (NaoEncontradoError, RegraDeNegocioError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.delete("/{triagem_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_triagem_invalida(triagem_id: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        service.deletar_triagem_invalida(triagem_id)
        return None
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))