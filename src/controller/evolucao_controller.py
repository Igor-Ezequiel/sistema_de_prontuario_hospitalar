from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.clinico_schema import EvolucaoCreate, EvolucaoUpdate
from src.repositori.EvolucaoRepositori import EvolucaoRepositori
from src.repositori.AtendimentoRepositori import AtendimentoRepository
from src.repositori.CID_Repositori import CIDRepository
from src.services.EvolucaoService import EvolucaoService
from src.exceptions import RegraDeNegocioError, NaoEncontradoError, PermissaoNegadaError
from src.deps import get_db

router = APIRouter(prefix="/evolucoes", tags=["Clínico - Evoluções"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def registrar(dados: EvolucaoCreate, db = Depends(get_db)):
    try:
        service = EvolucaoService(EvolucaoRepositori(db), AtendimentoRepository(db), CIDRepository(db))
        nova_evo = service.registrar_nova_evolucao(
            dados.atendimento_id, dados.medico_id, dados.relato, dados.dias_entubacao, dados.lista_cids
        )
        return {"mensagem": "Evolução registrada", "id": nova_evo.id}
    except (RegraDeNegocioError, NaoEncontradoError, PermissaoNegadaError) as e:
        codigo = status.HTTP_403_FORBIDDEN if isinstance(e, PermissaoNegadaError) else (
            status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST)
        raise HTTPException(status_code=codigo, detail=str(e))

@router.put("/{id_evolucao}")
def editar(id_evolucao: int, dados: EvolucaoUpdate, db = Depends(get_db)):
    try:
        service = EvolucaoService(EvolucaoRepositori(db), AtendimentoRepository(db), CIDRepository(db))
        service.atualizar_evolucao(id_evolucao, dados.medico_id, dados.relato, dados.dias_entubacao)
        return {"mensagem": "Evolução atualizada com sucesso"}
    except (RegraDeNegocioError, NaoEncontradoError, PermissaoNegadaError) as e:
        codigo = status.HTTP_403_FORBIDDEN if isinstance(e, PermissaoNegadaError) else (
            status.HTTP_404_NOT_FOUND if isinstance(e, NaoEncontradoError) else status.HTTP_400_BAD_REQUEST)
        raise HTTPException(status_code=codigo, detail=str(e))