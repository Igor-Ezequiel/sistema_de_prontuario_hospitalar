from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.clinico_schema import PrescricaoCreate, PrescricaoAplicar, PrescricaoResponse
from src.repositori.PrescricaoRepository import PrescricaoRepository
from src.service.PrecricaoService import PrescricaoService
from src.exceptions import NaoEncontradoError, RegraDeNegocioError
from src.deps import get_db

router = APIRouter(prefix="/prescricoes", tags=["Clínico - Prescrições"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def prescrever_medicamento(dados: PrescricaoCreate, db = Depends(get_db)):
    try:
        service = PrescricaoService(PrescricaoRepository(db))
        id_gerado = service.prescrever_medicamento(
            nome_medicamento=dados.nome_medicamento,
            dose=dados.dose,
            intervalo_horas=dados.intervalo_horas,
            evolucao_id=dados.evolucao_id
        )
        return {"mensagem": "Medicamento prescrito com sucesso", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{id_prescricao}/aplicar", response_model=PrescricaoResponse)
def aplicar_medicamento(id_prescricao: int, dados: PrescricaoAplicar, db = Depends(get_db)):
    try:
        service = PrescricaoService(PrescricaoRepository(db))
        return service.aplicar_medicamento(id_prescricao, dados.enfermeiro_id)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{id_prescricao}/cancelar")
def cancelar_prescricao(id_prescricao: int, db = Depends(get_db)):
    try:
        service = PrescricaoService(PrescricaoRepository(db))
        service.cancelar_prescricao(id_prescricao)
        return {"mensagem": "Prescrição cancelada com sucesso"}
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_prescricao}/detalhes", response_model=PrescricaoResponse)
def ver_detalhes_aplicacao(id_prescricao: int, db = Depends(get_db)):
    try:
        service = PrescricaoService(PrescricaoRepository(db))
        return service.ver_detalhes_aplicacao(id_prescricao)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))