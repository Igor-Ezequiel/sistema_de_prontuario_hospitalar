from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.equipe_schema import EnfermeiroCreate, EnfermeiroUpdate
from src.repositori.Equipe_Medica.EnfermeiroRepositori import EnfermeiroRepositori
from src.services.EnfermeiroService import EnfermeiroService
from src.exceptions import RegraDeNegocioError, NaoEncontradoError
from src.deps import get_db

router = APIRouter(prefix="/enfermeiros", tags=["Equipe Médica"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar(dados: EnfermeiroCreate, db = Depends(get_db)):
    try:
        service = EnfermeiroService(EnfermeiroRepositori(db))
        id_gerado = service.cadastrar_enfermeiro(dados.nome, dados.coren, dados.email, dados.senha)
        return {"mensagem": "Enfermeiro cadastrado", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id_enfermeiro}")
def atualizar(id_enfermeiro: int, dados: EnfermeiroUpdate, db = Depends(get_db)):
    try:
        service = EnfermeiroService(EnfermeiroRepositori(db))
        enfermeiro = service.atualizar_dados(id_enfermeiro, dados.nome, dados.coren)
        return {"mensagem": "Perfil atualizado", "nome": enfermeiro.nome}
    except (NaoEncontradoError, RegraDeNegocioError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.delete("/{id_enfermeiro}", status_code=status.HTTP_204_NO_CONTENT)
def inativar(id_enfermeiro: int, db = Depends(get_db)):
    try:
        service = EnfermeiroService(EnfermeiroRepositori(db))
        service.inativar_enfermeiro(id_enfermeiro)
    except (NaoEncontradoError, RegraDeNegocioError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))