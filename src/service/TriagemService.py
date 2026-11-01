from datetime import datetime
from src.models.Classes import Triagem, CorRisco, StatusAtendimento
from src.service.SistemaFilaPrioridade import fila_hospital

class TriagemService:
    def __init__(self, triagem_repo, atendimento_repo):
        self.triagem_repo = triagem_repo
        self.atendimento_repo = atendimento_repo

    def Criar_triagem(
        self, 
        atendimento_id: int, 
        enfermeiro_id: int, 
        pressao: str, 
        temperatura: float, 
        saturacao: int, 
        nova_cor: CorRisco
    ):
        ficha = self.atendimento_repo.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
            
            raise ValueError("O paciente não possui atendimento registrado.")

        if nova_cor == CorRisco.VERMELHO:
            
            raise ValueError("Risco VERMELHO é emergência! Use 'Classificar_Risco' direto no AtendimentoService.")

        if ficha.status != StatusAtendimento.AGUARDANDO_TRIAGEM.value:
            
            raise ValueError(f"O paciente não pode ser triado. Status atual: {ficha.status}")

        ficha.cor_risco = nova_cor
        ficha.status = StatusAtendimento.AGUARDANDO_MEDICO.value
        
        if not fila_hospital.Verificar_QuantidadeMax():
    
            fila_hospital.Inserir_Paciente(ficha)
    
            match nova_cor:
                case CorRisco.AZUL:
                    print("Azul: situações eletivas ou administrativas...")
                case CorRisco.VERDE:
                    print("Verde: pouco urgentes, com baixo risco...")
                case CorRisco.AMARELO:
                    print("Amarelo: urgência clínica, necessitam de atendimento...")
                case CorRisco.LARANJA:
                    print("Laranja: muita urgência, risco de agravamento rápido...") 
        else:
            print("A fila está cheia!")
                
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

        print("Triagem registrada e cor do atendimento atualizada com sucesso!")


    def buscar_triagens(self, atendimento_id: int) -> list[Triagem]:
        ficha = self.atendimento_repo.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
            raise ValueError("O paciente não possui atendimento registrado.")
            
        historico = self.triagem_repo.buscar_historico_por_atendimento(atendimento_id)
        
        if not historico:
            print("Nenhuma triagem registrada para este atendimento até o momento.")
            
        return historico


    def corrigir_erro_afericao(
        self, 
        triagem_id: int, 
        nova_pressao: str, 
        nova_temperatura: float, 
        nova_saturacao: int
    ):
        triagem_corrigida = Triagem(
            id_triagem=triagem_id,
            pressao=nova_pressao,
            temperatura=nova_temperatura,
            saturacao=nova_saturacao,
            data_hora=None 
        )
        
        
        self.triagem_repo.Atualizar_Triagem(triagem_corrigida)
        print(f"Triagem {triagem_id} corrigida com sucesso!")

    def deletar_triagem_invalida(self, triagem_id: int):
        self.triagem_repo.excluir_triagem_errada(triagem_id)
        print(f"Triagem {triagem_id} excluída do sistema.")