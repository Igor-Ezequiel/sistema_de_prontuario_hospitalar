from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.equipe_schema import MedicoCreate, MedicoUpdate, MedicoResponse
from src.repositori.Equipe_Medica.MedicoRepositori import MedicoRepositori
from src.services.MedicoService import MedicoService
from src.exceptions import RegraDeNegocioError, NaoEncontradoError
from src.deps import get_db
from datetime import datetime

router = APIRouter(prefix="/medicos", tags=["Equipe Médica"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar(dados: MedicoCreate, db = Depends(get_db)):
    try:
        service = MedicoService(MedicoRepositori(db))
        id_gerado = service.cadastrar_medico(dados.nome, dados.crm, dados.especialidade, dados.email, dados.senha)
        return {"mensagem": "Médico cadastrado", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id_medico}")
def atualizar(id_medico: int, dados: MedicoUpdate, db = Depends(get_db)):
    try:
        service = MedicoService(MedicoRepositori(db))
        medico = service.atualizar_dados(id_medico, dados.nome, dados.crm, dados.especialidade)
        return {"mensagem": "Perfil atualizado", "nome": medico.nome}
    except (NaoEncontradoError, RegraDeNegocioError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.delete("/{id_medico}", status_code=status.HTTP_204_NO_CONTENT)
def inativar(id_medico: int, db = Depends(get_db)):
    try:
        service = MedicoService(MedicoRepositori(db))
        service.inativar_medico(id_medico)
    except (NaoEncontradoError, RegraDeNegocioError) as e:
        codigo = status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=codigo, detail=str(e))

@router.get("/disponiveis")
def listar_disponiveis(inicio: datetime, fim: datetime, db = Depends(get_db)):
    try:
        service = MedicoService(MedicoRepositori(db))
        return service.buscar_medicos_para_plantao(inicio, fim)
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))