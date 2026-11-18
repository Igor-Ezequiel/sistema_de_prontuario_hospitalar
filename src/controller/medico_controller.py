from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import List
from src.schemas.equipe_schema import MedicoCreate, MedicoUpdate, MedicoResponse
from repositori.Equipe_Medica.MedicoRepository import MedicoRepositori
from src.service.MedicoService import MedicoService
from src.exceptions import NaoEncontradoError, RegraDeNegocioError
from src.deps import get_db

router = APIRouter(prefix="/medicos", tags=["Equipe Médica - Médicos"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def cadastrar_medico(dados: MedicoCreate, db = Depends(get_db)):
    try:
        service = MedicoService(MedicoRepositori(db))
        id_gerado = service.cadastrar_medico(
            nome=dados.nome,
            crm=dados.crm,
            especialidade=dados.especialidade,
            email=dados.email,
            senha_plana=dados.senha
        )
        return {"mensagem": "Médico cadastrado com sucesso", "id": id_gerado}
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/disponiveis", response_model=List[MedicoResponse])
def buscar_medicos_para_plantao(inicio: datetime, fim: datetime, db = Depends(get_db)):
    try:
        service = MedicoService(MedicoRepositori(db))
        return service.buscar_medicos_para_plantao(inicio, fim)
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{id_medico}", response_model=MedicoResponse)
def buscar_medico(id_medico: int, db = Depends(get_db)):
    try:
        service = MedicoService(MedicoRepositori(db))
        return service.buscar_medico_valido(id_medico)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id_medico}", response_model=MedicoResponse)
def atualizar_medico(id_medico: int, dados: MedicoUpdate, db = Depends(get_db)):
    try:
        service = MedicoService(MedicoRepositori(db))
        return service.atualizar_dados(id_medico, dados.nome, dados.crm, dados.especialidade)
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id_medico}", status_code=status.HTTP_204_NO_CONTENT)
def inativar_medico(id_medico: int, db = Depends(get_db)):
    try:
        service = MedicoService(MedicoRepositori(db))
        service.inativar_medico(id_medico)
        return None
    except NaoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RegraDeNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))