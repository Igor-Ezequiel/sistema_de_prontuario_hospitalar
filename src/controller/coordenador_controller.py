from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.equipe_schema import CoordenadorCreate, CoordenadorUpdate, CoordenadorResponse
from src.repositori.Equipe_Medica.CoordenadorRepository import CoordenadorRepositori
from src.service.CoordenadorService import CoordenadorService
from src.exceptions import NaoEncontradoError, RegraDeNegocioError
from src.deps import get_db

router = APIRouter(prefix="/coordenadores", tags=["Equipe Médica - Coordenadores"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_coordenador(dados: CoordenadorCreate, db = Depends(get_db)):
    try:
        service = CoordenadorService(CoordenadorRepositori(db))
        id_gerado = service.cadastrar_coordenador(dados.nome, dados.setor_responsavel, dados.email, dados.senha)
        return {"mensagem": "Coordenador cadastrado com sucesso", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_coordenador}", response_model=CoordenadorResponse)
def buscar_coordenador(id_coordenador: int, db = Depends(get_db)):
    try:
        service = CoordenadorService(CoordenadorRepositori(db))
        return service.buscar_coordenador_valido(id_coordenador)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id_coordenador}", response_model=CoordenadorResponse)
def atualizar_coordenador(id_coordenador: int, dados: CoordenadorUpdate, db = Depends(get_db)):
    try:
        service = CoordenadorService(CoordenadorRepositori(db))
        return service.atualizar_dados(id_coordenador, dados.nome, dados.setor_responsavel)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id_coordenador}", status_code=status.HTTP_204_NO_CONTENT)
def inativar_coordenador(id_coordenador: int, db = Depends(get_db)):
    try:
        service = CoordenadorService(CoordenadorRepositori(db))
        service.inativar_coordenador(id_coordenador)
        return None
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))