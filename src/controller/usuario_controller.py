from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.equipe_schema import (
    LoginRequest, 
    UsuarioCreate, 
    UsuarioCredenciaisUpdate, 
    UsuarioResponse
)
from repositori.Equipe_Medica.UsuarioRepository import UsuarioRepositori
from src.service.UsuarioService import UsuarioService
from src.exceptions import NaoEncontradoError, RegraDeNegocioError, PermissaoNegadaError
from src.deps import get_db

router = APIRouter(prefix="/usuarios", tags=["Autenticação e Usuários"])

@router.post("/login", response_model=UsuarioResponse)
def fazer_login(dados: LoginRequest, db = Depends(get_db)):
    try:
        service = UsuarioService(UsuarioRepositori(db))
        return service.fazer_login(dados.email, dados.senha)
    except PermissaoNegadaError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: UsuarioCreate, db = Depends(get_db)):
    try:
        service = UsuarioService(UsuarioRepositori(db))
        id_gerado = service.Criar_Usuario(dados.email, dados.senha, dados.cargo, dados.ativo)
        return {"mensagem": "Usuário criado com sucesso", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_usuario}", response_model=UsuarioResponse)
def buscar_usuario(id_usuario: int, db = Depends(get_db)):
    try:
        service = UsuarioService(UsuarioRepositori(db))
        return service.Buscar_Usuario(id_usuario)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{id_usuario}/credenciais")
def atualizar_credenciais(id_usuario: int, dados: UsuarioCredenciaisUpdate, db = Depends(get_db)):
    try:
        service = UsuarioService(UsuarioRepositori(db))
        service.Atualizar_Credenciais(id_usuario, dados.email, dados.senha)
        return {"mensagem": "Credenciais atualizadas com sucesso"}
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{id_usuario}/desativar")
def desativar_usuario(id_usuario: int, db = Depends(get_db)):
    try:
        service = UsuarioService(UsuarioRepositori(db))
        service.Desativar_Usuario(id_usuario)
        return {"mensagem": "Usuário desativado com sucesso"}
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{id_usuario}/reativar")
def reativar_usuario(id_usuario: int, db = Depends(get_db)):
    try:
        service = UsuarioService(UsuarioRepositori(db))
        service.Reativar_Usuario(id_usuario)
        return {"mensagem": "Usuário reativado com sucesso"}
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))