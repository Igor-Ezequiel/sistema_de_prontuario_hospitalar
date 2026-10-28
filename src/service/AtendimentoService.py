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
            paciente_id=paciente_id,
            data_alta=None,
            medico_id=None
        )

        # CORRIGIDO: Estava escrito self.repository (com 'y')
        atendimento_id_gerado = self.repositori.criar_novo_atendimento(nova_ficha)
        return atendimento_id_gerado
    
    def buscar_atendimento(self, atendimento_id: int) -> Atendimento:
        # CORRIGIDO: Estava escrito self.repository (com 'y')
        ficha = self.repositori.buscar_simples_por_id(atendimento_id)

        if ficha is None:
            raise ValueError("Erro: O paciente não possui atendimento registrado.")

        return ficha
    
    def Classificar_Risco(self, atendimento_id: int, nova_cor: CorRisco):
        ficha = self.repositori.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
            raise ValueError("O paciente não possui atendimento registrado.")
        
        # CORRIGIDO: Comparava ficha.cor_risco em vez do parâmetro nova_cor, e não atualizava a cor!
        if nova_cor == CorRisco.VERMELHO:
            print("Emergência absoluta: risco iminente de morte, intervenção médica imediata.")
            ficha.status = StatusAtendimento.EM_ATENDIMENTO.value
        else:
            ficha.status = StatusAtendimento.AGUARDANDO_TRIAGEM.value  # CORRIGIDO: Faltava o .value
                
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
          
        # CORRIGIDO: Passava o objeto 'ficha', mas o repositório espera apenas o 'atendimento_id'
        self.repositori.deletar_atendimento(atendimento_id)