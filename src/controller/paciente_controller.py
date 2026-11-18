from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.paciente_schema import PacienteCreate, PacienteUpdate, PacienteResponse
from src.repositori.Equipe_Medica.PacienteRepositori import PacienteRepositori
from src.repositori.Equipe_Medica.UsuarioRepositori import UsuarioRepositori
from src.service.PacienteService import PacienteService
from src.exceptions import NaoEncontradoError, RegraDeNegocioError
from src.deps import get_db

router = APIRouter(prefix="/pacientes", tags=["Recepção - Pacientes"])

def obter_service(db) -> PacienteService:
    return PacienteService(PacienteRepositori(db), UsuarioRepositori(db))

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_paciente(dados: PacienteCreate, db = Depends(get_db)):
    try:
        service = obter_service(db)
        id_gerado = service.cadastrar_paciente(dados.nome, dados.cpf, dados.data_nascimento)
        return {"mensagem": "Paciente cadastrado com sucesso", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_paciente}", response_model=PacienteResponse)
def buscar_paciente(id_paciente: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.buscar_paciente_valido(id_paciente)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id_paciente}", response_model=PacienteResponse)
def atualizar_paciente(id_paciente: int, dados: PacienteUpdate, db = Depends(get_db)):
    try:
        service = obter_service(db)
        return service.atualizar_dados(
            id_paciente=id_paciente,
            nome=dados.nome,
            cpf=dados.cpf,
            data_nascimento=dados.data_nascimento,
            usuario_id=dados.usuario_id
        )
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id_paciente}", status_code=status.HTTP_204_NO_CONTENT)
def inativar_paciente(id_paciente: int, db = Depends(get_db)):
    try:
        service = obter_service(db)
        service.inativar_paciente(id_paciente)
        return None
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))