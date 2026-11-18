from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.atendimento_schema import AtendimentoCreate, AtendimentoUpdate, AtendimentoResponse
from src.repositori.AtendimentoRepositori import AtendimentoRepository
from src.services.AtendimentoService import AtendimentoService
from src.exceptions import RegraDeNegocioError, NaoEncontradoError
from src.deps import get_db

router = APIRouter(prefix="/atendimentos", tags=["Recepção"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def abrir_ficha(dados: AtendimentoCreate, db = Depends(get_db)):
    try:
        service = AtendimentoService(AtendimentoRepository(db))
        id_gerado = service.abrir_ficha(dados.paciente_id, dados.cor_risco.value)
        return {"mensagem": "Atendimento aberto", "id": id_gerado}
    except (RegraDeNegocioError, NaoEncontradoError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.put("/{id_atendimento}")
def atualizar_status(id_atendimento: int, dados: AtendimentoUpdate, db = Depends(get_db)):
    try:
        service = AtendimentoService(AtendimentoRepository(db))
        service.atualizar_status(id_atendimento, dados.status.value, dados.cor_risco.value, dados.medico_id)
        return {"mensagem": "Status atualizado"}
    except (NaoEncontradoError, RegraDeNegocioError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.get("/{id_atendimento}", response_model=AtendimentoResponse)
def buscar_prontuario_completo(id_atendimento: int, db = Depends(get_db)):
    try:
        service = AtendimentoService(AtendimentoRepository(db))
        return service.buscar_ficha_completa(id_atendimento)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))