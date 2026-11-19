from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.atendimento_schema import PlantaoCreate, PlantaoUpdate, PlantaoResponse
from src.repositori.PlantaoRepository import PlantaoRepository
from src.repositori.Equipe_Medica.MedicoRepository import MedicoRepository
from src.service.PlantaoService import PlantaoService
from src.exceptions import NaoEncontradoError, RegraDeNegocioError
from src.deps import get_db

router = APIRouter(prefix="/plantoes", tags=["Escala - Plantões"])

def obter_service(db) -> PlantaoService:
    return PlantaoService(PlantaoRepository(db), MedicoRepository(db))

@router.post("/", status_code=status.HTTP_201_CREATED)
def alocar_medico_no_plantao(dados: PlantaoCreate, db = Depends(get_db)):
    try:
        service = obter_service(db)
        id_gerado = service.alocar_medico_no_plantao(
            coordenador_id=dados.coordenador_id,
            medico_id=dados.medico_id,
            setor_ala=dados.setor_ala,
            data_hora_inicio=dados.data_hora_inicio,
            data_hora_fim=dados.data_hora_fim
        )
        return {"mensagem": "Médico alocado no plantão com sucesso", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_plantao}", response_model=PlantaoResponse)
def buscar_plantao_por_id(id_plantao: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_plantao_por_id(id_plantao)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{id_plantao}/detalhes", response_model=PlantaoResponse)
def buscar_detalhes_do_plantao(id_plantao: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_detalhes_do_plantao(id_plantao)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{id_plantao}")
def atualizar_plantao(id_plantao: int, dados: PlantaoUpdate, db = Depends(get_db)):
    try:
        service = obter_service(db)
        service.atualizar_plantao(
            id_plantao=id_plantao,
            coordenador_id=dados.coordenador_id,
            medico_id=dados.medico_id,
            setor_ala=dados.setor_ala,
            data_hora_inicio=dados.data_hora_inicio,
            data_hora_fim=dados.data_hora_fim
        )
        return {"mensagem": "Plantão atualizado com sucesso"}
    except (NaoEncontradoError, RegraDeNegocioError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.delete("/{id_plantao}", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_plantao(id_plantao: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        service.cancelar_plantao(id_plantao)
        return None
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))