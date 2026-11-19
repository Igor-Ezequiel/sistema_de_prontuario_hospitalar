from datetime import datetime
from src.models.Classes import Evolucao, CID, StatusAtendimento
from src.repositori.EvolucaoRepository import EvolucaoRepository
from src.repositori.AtendimentoRepository import AtendimentoRepository
from src.repositori.CID_Repository import CIDRepository
from src.exceptions import (
    NaoEncontradoError,
    RegraDeNegocioError,
    PermissaoNegadaError
)

class EvolucaoService:
    
    def __init__(
        self, 
        evolucao_repo: EvolucaoRepository, 
        atendimento_repo: AtendimentoRepository, 
        cid_repo: CIDRepository
    ):
        self.evolucao_repo = evolucao_repo
        self.atendimento_repo = atendimento_repo
        self.cid_repo = cid_repo

    def registrar_nova_evolucao(
        self, 
        atendimento_id: int, 
        medico_id: int, 
        relato: str, 
        dias_entubacao: int = 0, 
        lista_cids: list[str] = None
    ) -> Evolucao:
        
        ficha = self.atendimento_repo.buscar_simples_por_id(atendimento_id)
        if ficha is None:
            raise NaoEncontradoError("O paciente não possui atendimento registrado.")

        
        if ficha.status != StatusAtendimento.EM_ATENDIMENTO.value:
            raise RegraDeNegocioError(
                f"Não é possível registrar evolução. Status atual do atendimento: {ficha.status}."
            )

        if ficha.medico_id != medico_id:
            raise PermissaoNegadaError(
                "Acesso negado: Apenas o médico responsável pelo prontuário pode registrar evoluções."
            )

        if not relato or not relato.strip():
            raise RegraDeNegocioError("O relato clínico da evolução não pode estar vazio.")

        
        objetos_cid = []
        if lista_cids:
            for codigo in lista_cids:
                cid_encontrado = self.cid_repo.buscar_simples_por_id(codigo)
                if cid_encontrado is None:
                    raise NaoEncontradoError(f"O código CID '{codigo}' não existe no sistema.")
                objetos_cid.append(cid_encontrado)

        
        nova_evolucao = Evolucao(
            id_evolucao=None,
            relato=relato,
            data_hora=datetime.now(),
            dias_entubacao=dias_entubacao,
            atendimento_id=atendimento_id,
            medico_id=medico_id
        )
        nova_evolucao.id = self.evolucao_repo.Inserir_Evolucao(nova_evolucao)

        
        for cid_obj in objetos_cid:
            self.evolucao_repo.vincular_diagnostico(nova_evolucao.id, cid_obj.codigo)
            nova_evolucao.diagnosticos.append(cid_obj)

        return nova_evolucao

    def vincular_novo_diagnostico(self, id_evolucao: int, medico_id: int, codigo_cid: str) -> CID:
        
        evolucao = self.evolucao_repo.buscar_simples_por_id(id_evolucao)
        if evolucao is None:
            raise NaoEncontradoError("Evolução clínica não encontrada no sistema.")

        if evolucao.medico_id != medico_id:
            raise PermissaoNegadaError("Apenas o médico autor da evolução pode adicionar diagnósticos a ela.")

        cid_encontrado = self.cid_repo.buscar_simples_por_id(codigo_cid)
        if cid_encontrado is None:
            raise NaoEncontradoError(f"O código CID '{codigo_cid}' não existe no sistema.")

        
        cids_atuais = self.evolucao_repo.buscar_diagnosticos_por_evolucao(id_evolucao)
        for cid_atual in cids_atuais:
            if cid_atual.codigo == codigo_cid:
                raise RegraDeNegocioError(f"O CID '{codigo_cid}' já está vinculado a esta evolução.")

        self.evolucao_repo.vincular_diagnostico(id_evolucao, codigo_cid)
        return cid_encontrado

    def buscar_evolucao_por_id(self, id_evolucao: int) -> Evolucao:
        
        evolucao = self.evolucao_repo.buscar_simples_por_id(id_evolucao)
        if evolucao is None:
            raise NaoEncontradoError("Evolução clínica não encontrada no sistema.")

        evolucao.diagnosticos = self.evolucao_repo.buscar_diagnosticos_por_evolucao(id_evolucao)
        
        evolucao.prescricoes = self.evolucao_repo.buscar_prescricoes_por_evolucao(id_evolucao)
        
        return evolucao

    def buscar_historico_por_atendimento(self, atendimento_id: int) -> list[Evolucao]:
        
        ficha = self.atendimento_repo.buscar_simples_por_id(atendimento_id)
        if ficha is None:
            raise NaoEncontradoError("O paciente não possui atendimento registrado.")

        historico = self.evolucao_repo.buscar_historico_por_atendimento(atendimento_id)
        if not historico:
            raise NaoEncontradoError("Nenhuma evolução clínica registrada para este atendimento até o momento.")

        return historico

    def atualizar_evolucao(
        self, 
        id_evolucao: int, 
        medico_id: int, 
        novo_relato: str, 
        novos_dias_entubacao: int = None
    ) -> Evolucao:
        
        evolucao = self.evolucao_repo.buscar_simples_por_id(id_evolucao)
        if evolucao is None:
            raise NaoEncontradoError("Evolução clínica não encontrada no sistema.")

        if evolucao.medico_id != medico_id:
            raise PermissaoNegadaError("Apenas o médico autor pode editar esta evolução clínica.")

        if not novo_relato or not novo_relato.strip():
            raise RegraDeNegocioError("O relato clínico não pode ficar vazio.")

        evolucao.relato = novo_relato
        if novos_dias_entubacao is not None:
            evolucao.dias_entubacao = novos_dias_entubacao

        self.evolucao_repo.Atualizar_Evolucao(evolucao)
        return evolucao

    def excluir_evolucao(self, id_evolucao: int, medico_id: int):
        
        evolucao = self.evolucao_repo.buscar_simples_por_id(id_evolucao)
        if evolucao is None:
            raise NaoEncontradoError("Evolução clínica não encontrada no sistema.")

        if evolucao.medico_id != medico_id:
            raise PermissaoNegadaError("Apenas o médico autor pode excluir esta evolução clínica.")

        self.evolucao_repo.excluir_evolucao(id_evolucao)