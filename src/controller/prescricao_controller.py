from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.clinico_schema import PrescricaoCreate
from src.repositori.Equipe_Medica.PrescricaoRepositori import PrescricaoRepositori
from src.services.PrescricaoService import PrescricaoService
from src.exceptions import RegraDeNegocioError, NaoEncontradoError
from src.deps import get_db

router = APIRouter(prefix="/prescricoes", tags=["Clínico - Prescrições"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def prescrever(dados: PrescricaoCreate, db = Depends(get_db)):
    try:
        service = PrescricaoService(PrescricaoRepositori(db))
        id_gerado = service.prescrever_medicamento(
            dados.nome_medicamento, dados.dose, dados.intervalo_horas, dados.evolucao_id
        )
        return {"mensagem": "Medicamento prescrito", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{id_prescricao}/aplicar")
def aplicar(id_prescricao: int, enfermeiro_id: int, db = Depends(get_db)):
    try:
        service = PrescricaoService(PrescricaoRepositori(db))
        service.aplicar_medicamento(id_prescricao, enfermeiro_id)
        return {"mensagem": "Medicação aplicada com sucesso"}
    except (RegraDeNegocioError, NaoEncontradoError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.patch("/{id_prescricao}/cancelar")
def cancelar(id_prescricao: int, db = Depends(get_db)):
    try:
        service = PrescricaoService(PrescricaoRepositori(db))
        service.cancelar_prescricao(id_prescricao)
        return {"mensagem": "Prescrição suspensa"}
    except (RegraDeNegocioError, NaoEncontradoError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))