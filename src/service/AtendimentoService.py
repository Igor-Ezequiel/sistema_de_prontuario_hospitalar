from datetime import datetime
from src.service.SistemaFilaPrioridade import fila_hospital
from src.repositori.AtendimentoRepositori import AtendimentoRepository
from src.repositori.PlantaoRepositori import PlantaoRepositori
from src.repositori.PermissaoExtraRepositori import PermissaoExtrarepositori
from src.repositori.Equipe_Medica.MedicoRepositori import MedicoRepositori
from src.models.Classes import (
    StatusAtendimento,
    CorRisco,
    Atendimento,
)
from src.exceptions import NaoEncontradoError, RegraDeNegocioError


class AtendimentoService:
    
    def __init__(self, repositori: AtendimentoRepository, repositori_medico: MedicoRepositori, 
                 repositori_plantao: PlantaoRepositori, repositori_permissao_extra: PermissaoExtrarepositori):
        self.repositori = repositori
        self.repositori_medico = repositori_medico
        self.repositori_plantao = repositori_plantao
        self.repositori_permissao = repositori_permissao_extra
        

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

        atendimento_id_gerado = self.repositori.criar_novo_atendimento(nova_ficha)
        return atendimento_id_gerado
    
    
    def buscar_atendimento(self, atendimento_id: int) -> Atendimento:
        ficha = self.repositori.buscar_simples_por_id(atendimento_id)

        if ficha is None:
            raise NaoEncontradoError("Erro: O paciente não possui atendimento registrado.")

        return ficha
    
    
    def Classificar_Risco(self, atendimento_id: int, nova_cor: CorRisco):
        ficha = self.repositori.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
            raise NaoEncontradoError("O paciente não possui atendimento registrado.")
        
        ficha.cor_risco = nova_cor
        
        if nova_cor == CorRisco.VERMELHO:
            if not fila_hospital.Verificar_QuantidadeMax():
                RegraDeNegocioError("Emergência absoluta: risco iminente de morte, intervenção médica imediata.")
                ficha.status = StatusAtendimento.EM_ATENDIMENTO.value
                fila_hospital.Inserir_Paciente(ficha)
            
        else:
            ficha.status = StatusAtendimento.AGUARDANDO_TRIAGEM.value
                
        ficha.cor_risco = nova_cor.value
        self.repositori.atualizar_dados_atendimento(ficha)
    
    
    def dar_alta(self, atendimento_id: int):
        ficha = self.repositori.buscar_simples_por_id(atendimento_id)
    
        if ficha is None:
            raise NaoEncontradoError("O paciente não possui atendimento registrado.")
        
        if ficha.status == StatusAtendimento.ALTA.value:
            raise RegraDeNegocioError("Este paciente já recebeu alta anteriormente.")
        
        if ficha.status == StatusAtendimento.AGUARDANDO_TRIAGEM.value:
            raise RegraDeNegocioError("O paciente não pode receber alta antes de ser atendido.")

        ficha.status = StatusAtendimento.ALTA.value
        ficha.data_alta = datetime.now()

        self.repositori.atualizar_dados_atendimento(ficha)
        
        
    def Deletar_Atendimento(self, atendimento_id: int):
        ficha = self.repositori.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
            raise NaoEncontradoError("O paciente não possui atendimento registrado.")
          
        self.repositori.deletar_atendimento(atendimento_id)
        
        
    def Chamar_Paciente(self, medico_id: int):
        hora_atual = datetime.now()
        medico_plantao = self.repositori_plantao.verificar_plantao_ativo(medico_id, hora_atual)
            
        if not medico_plantao:
            raise RegraDeNegocioError("Este médico não está em um plantão ativo no momento!")
        
        atender_proximo_paciente = fila_hospital.Atender_Proximo_Paciente()
        
        if atender_proximo_paciente is None:
            raise RegraDeNegocioError("Não há pacientes aguardando na fila no momento.")
        
        ficha = self.repositori.buscar_simples_por_id(atender_proximo_paciente.id)
        ficha.status = StatusAtendimento.EM_ATENDIMENTO.value
        ficha.medico_id = medico_id
        self.repositori.atualizar_dados_atendimento(ficha)
            
        return ficha
    
    
    def conceder_permissao_extra(self, atendimento_id: int, coordenador_id: int, medico_id: int, motivo: str):
        ficha = self.repositori.buscar_simples_por_id(atendimento_id)
        
        if ficha is None:
            raise NaoEncontradoError("O paciente não possui atendimento registrado.")
        
        if ficha.medico_id == medico_id:
            raise RegraDeNegocioError("Inválido: O prontuário já está alocado para este mesmo médico!")
        
        ficha.medico_id = medico_id 
    
        self.repositori.atualizar_dados_atendimento(ficha)
        self.repositori_permissao.inserir_permissao(atendimento_id, medico_id, coordenador_id, motivo)
        
        return ficha