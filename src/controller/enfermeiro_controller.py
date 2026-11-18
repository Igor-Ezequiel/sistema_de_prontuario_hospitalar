from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.equipe_schema import EnfermeiroCreate, EnfermeiroUpdate, EnfermeiroResponse
from repositori.Equipe_Medica.EnfermeiroRepository import EnfermeiroRepositori
from src.service.EnfermeiroService import EnfermeiroService
from src.exceptions import NaoEncontradoError, RegraDeNegocioError
from src.deps import get_db

router = APIRouter(prefix="/enfermeiros", tags=["Equipe Médica - Enfermeiros"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_enfermeiro(dados: EnfermeiroCreate, db = Depends(get_db)):
    try:
        service = EnfermeiroService(EnfermeiroRepositori(db))
        id_gerado = service.cadastrar_enfermeiro(dados.nome, dados.coren, dados.email, dados.senha)
        return {"mensagem": "Enfermeiro cadastrado com sucesso", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_enfermeiro}", response_model=EnfermeiroResponse)
def buscar_enfermeiro(id_enfermeiro: int, db = Depends(get_db)):
    try:
        service = EnfermeiroService(EnfermeiroRepositori(db))
        return service.buscar_enfermeiro_valido(id_enfermeiro)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id_enfermeiro}", response_model=EnfermeiroResponse)
def atualizar_enfermeiro(id_enfermeiro: int, dados: EnfermeiroUpdate, db = Depends(get_db)):
    try:
        service = EnfermeiroService(EnfermeiroRepositori(db))
        return service.atualizar_dados(id_enfermeiro, dados.nome, dados.coren)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id_enfermeiro}", status_code=status.HTTP_204_NO_CONTENT)
def inativar_enfermeiro(id_enfermeiro: int, db = Depends(get_db)):
    try:
        service = EnfermeiroService(EnfermeiroRepositori(db))
        service.inativar_enfermeiro(id_enfermeiro)
        return None
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))