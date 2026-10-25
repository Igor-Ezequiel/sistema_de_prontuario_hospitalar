# Caminho: pasta src -> pasta models -> arquivo Classes.py
from datetime import datetime
from src.repositori.AtendimentoRepositori import AtendimentoRepository
from src.models.Classes import (
    StatusAtendimento,
    CorRisco,
    Atendimento
)

class AtendimentoService:
    
    def __init__(self, repositori: AtendimentoRepository):
        self.repositori = repositori


    def criar_atendimento(self, paciente_id: int) -> int:
        
        nova_ficha = Atendimento(
            atendimento_id=None,
            status=StatusAtendimento.AGUARDANDO_TRIAGEM.value,
            cor_risco=CorRisco.CINZA.value,
            data_entrada=datetime.now(),
            data_alta=None,
            paciente_id=paciente_id,
            medico_id=None
        )

        atendimento_id_gerado = self.repository.criar_novo_atendimento(nova_ficha)
        return atendimento_id_gerado
    
    
    def buscar_atendimento(self, atendimento_id: int) -> Atendimento:
        
        ficha = self.repository.buscar_simples_por_id(atendimento_id)

        if ficha is None:
            raise ValueError("Erro: O paciente não possui atendimento registrado.")

        return ficha
    
    
    def Classificar_Risco(self, atendimento_id: int, nova_cor: CorRisco):
            
        ficha = self.repositori.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
            raise ValueError("O paciente não possui atendimento registrado.")
        
        match nova_cor:
            
            case CorRisco.AZUL:
                                        
                print("situações eletivas ou administrativas, que não deveriam ser resolvidas em uma UPA ou serviço de urgência, mas sim na Atenção Primária à Saúde (APS).")
                ficha.status = StatusAtendimento.AGUARDANDO_TRIAGEM.value
                
            case CorRisco.VERDE:
                            
                print("pouco urgentes, com baixo risco de agravamento e que não requerem atendimento médico imediato. Geralmente, são queixas crônicas, desconfortos leves ou condições autolimitadas.")
                ficha.status = StatusAtendimento.AGUARDANDO_TRIAGEM.value   
            case CorRisco.AMARELO:
            
                print("urgência clínica, que necessitam de atendimento, mas sem risco iminente à vida naquele momento. São casos que exigem atenção médica preferencial, mas que podem aguardar por um curto período.")
                ficha.status = StatusAtendimento.AGUARDANDO_TRIAGEM.value   
            case CorRisco.LARANJA:
                
                print("muita urgência, com risco de agravamento clínico rápido, embora ainda haja sinais vitais presentes e relativa estabilidade momentânea.")
                ficha.status = StatusAtendimento.AGUARDANDO_TRIAGEM.value   
            case CorRisco.VERMELHO:
            
                print("emergência absoluta, ou seja, risco iminente de morte ou situação de saúde que exige intervenção imediata da equipe médica.")
                ficha.status = StatusAtendimento.EM_ATENDIMENTO.value
                
        ficha.cor_risco = nova_cor.value
    
        self.repositori.atualizar_dados_atendimento(ficha)
    
    
    def dar_alta(self, atendimento_id: int):

        ficha = self.repositori.buscar_simples_por_id(atendimento_id)
    
        if ficha is None:
            raise ValueError("O paciente não possui atendimento registrado.")
        
        if ficha.status == StatusAtendimento.ALTA.value:
            raise ValueError("Este paciente já recebeu alta anteriormente.")
        
        if ficha.status == StatusAtendimento.AGUARDANDO_TRIAGEM.value:
            raise ValueError("O paciente não pode receber alta antes de ser atendido.")

   
        ficha.status = StatusAtendimento.ALTA.value
        ficha.data_alta = datetime.now()

        self.repositori.atualizar_dados_atendimento(ficha)
        
        
    def Deletar_Atendimento(self, atendimento_id: int):
        
        ficha = self.repositori.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
             raise ValueError("O paciente não possui atendimento registrado.")
         
        
        self.repositori.deletar_atendimento(ficha)