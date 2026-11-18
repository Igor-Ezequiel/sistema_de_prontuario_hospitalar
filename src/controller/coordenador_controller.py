from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.equipe_schema import CoordenadorCreate, CoordenadorUpdate
from src.repositori.Equipe_Medica.CoordenadorRepositori import CoordenadorRepositori
from src.services.CoordenadorService import CoordenadorService
from src.exceptions import RegraDeNegocioError, NaoEncontradoError
from src.deps import get_db

router = APIRouter(prefix="/coordenadores", tags=["Equipe Médica"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar(dados: CoordenadorCreate, db = Depends(get_db)):
    try:
        service = CoordenadorService(CoordenadorRepositori(db))
        id_gerado = service.cadastrar_coordenador(dados.nome, dados.setor_responsavel, dados.email, dados.senha)
        return {"mensagem": "Coordenador cadastrado", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id_coordenador}")
def atualizar(id_coordenador: int, dados: CoordenadorUpdate, db = Depends(get_db)):
    try:
        service = CoordenadorService(CoordenadorRepositori(db))
        coordenador = service.atualizar_dados(id_coordenador, dados.nome, dados.setor_responsavel)
        return {"mensagem": "Perfil atualizado", "nome": coordenador.nome}
    except (NaoEncontradoError, RegraDeNegocioError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.delete("/{id_coordenador}", status_code=status.HTTP_204_NO_CONTENT)
def inativar(id_coordenador: int, db = Depends(get_db)):
    try:
        service = CoordenadorService(CoordenadorRepositori(db))
        service.inativar_coordenador(id_coordenador)
    except (NaoEncontradoError, RegraDeNegocioError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))