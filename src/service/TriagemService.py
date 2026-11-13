from datetime import datetime
from src.models.Classes import Triagem, CorRisco, StatusAtendimento
from src.service.SistemaFilaPrioridade import fila_hospital
from src.exceptions import NaoEncontradoError, RegraDeNegocioError


class TriagemService:
    def __init__(self, triagem_repo, atendimento_repo):
        self.triagem_repo = triagem_repo
        self.atendimento_repo = atendimento_repo

    
    def Criar_triagem(self, atendimento_id: int, enfermeiro_id: int, pressao: str, temperatura: float, saturacao: int, nova_cor: CorRisco):
        
        ficha = self.atendimento_repo.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
            raise NaoEncontradoError("O paciente não possui atendimento registrado.")

        if nova_cor == CorRisco.VERMELHO:
            raise RegraDeNegocioError("Risco VERMELHO é emergência! Use 'Classificar_Risco' direto no AtendimentoService.")

        if ficha.status != StatusAtendimento.AGUARDANDO_TRIAGEM.value:
            raise RegraDeNegocioError(f"O paciente não pode ser triado. Status atual: {ficha.status}")

        ficha.cor_risco = nova_cor
        ficha.status = StatusAtendimento.AGUARDANDO_MEDICO.value
        
        
        fila_hospital.Inserir_Paciente(ficha)
                
        nova_triagem = Triagem(
            id_triagem=None,
            pressao=pressao,
            temperatura=temperatura,
            saturacao=saturacao,
            data_hora=datetime.now(),
            atendimento_id=atendimento_id,
            enfermeiro_id=enfermeiro_id
        )

        self.triagem_repo.inserir_triagem(nova_triagem)
        ficha.cor_risco = nova_cor.value
        self.atendimento_repo.atualizar_dados_atendimento(ficha)

        
        return nova_triagem
        

    def buscar_triagem_por_id(self, id_triagem: int) -> Triagem:
        triagem = self.triagem_repo.buscar_por_id(id_triagem)
        
        if not triagem:
            raise NaoEncontradoError("Triagem não encontrada no sistema.")
            
        return triagem
    
    def buscar_historico(self, atendimento_id: int) -> list[Triagem]:
        ficha = self.atendimento_repo.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
            raise NaoEncontradoError("O paciente não possui atendimento registrado.")
            
        historico = self.triagem_repo.buscar_historico_por_atendimento(atendimento_id)
        
        if not historico:
            raise NaoEncontradoError("Nenhuma triagem registrada para este atendimento até o momento.")
            
        return historico
    
    def atualizar_triagem(self, triagem_id: int, nova_pressao: str, nova_temperatura: float, nova_saturacao: int):
        triagem_corrigida = Triagem(
            id_triagem=triagem_id,
            pressao=nova_pressao,
            temperatura=nova_temperatura,
            saturacao=nova_saturacao,
            data_hora=None 
        )
        
        self.triagem_repo.Atualizar_Triagem(triagem_corrigida)

    def deletar_triagem_invalida(self, triagem_id: int):
        self.triagem_repo.excluir_triagem_errada(triagem_id)
       