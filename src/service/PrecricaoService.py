from datetime import datetime
from src.models.Classes import Prescricao, StatusPrescricao
from src.repositori.PrescricaoRepository import PrescricaoRepository
from src.exceptions import NaoEncontradoError, RegraDeNegocioError

class PrescricaoService:
    def __init__(self, prescricao_repo: PrescricaoRepository):
        self.prescricao_repo = prescricao_repo

    def buscar_prescricao_valida(self, id_prescricao: int) -> Prescricao:
        """
        O 'Leão de Chácara': Garante que a prescrição existe antes de qualquer ação.
        """
        prescricao = self.prescricao_repo.buscar_por_id(id_prescricao)
        
        if not prescricao:
            raise NaoEncontradoError("Prescrição médica não encontrada no sistema.")
            
        return prescricao

    
    def prescrever_medicamento(self, nome_medicamento: str, dose: str, intervalo_horas: int, evolucao_id: int) -> int:
        """
        Ação exclusiva do Médico durante a consulta/evolução.
        """
        if not nome_medicamento or not dose:
            raise RegraDeNegocioError("O nome do medicamento e a dose são obrigatórios para a prescrição.")

        nova_prescricao = Prescricao(
            id_prescricao=None,
            nome_medicamento=nome_medicamento,
            dose=dose,
            intervalo_horas=intervalo_horas,
            status=StatusPrescricao.PENDENTE.value, 
            evolucao_id=evolucao_id,
            enfermeiro_id=None,          
            data_hora_aplicacao=None     
        ) 
        
        return self.prescricao_repo.inserir_prescricao(nova_prescricao)


    def cancelar_prescricao(self, id_prescricao: int):
        """
        Ação do Médico caso ele mude de ideia ou o paciente tenha alta.
        """
        prescricao = self.buscar_prescricao_valida(id_prescricao)

       
        if prescricao.status == StatusPrescricao.APLICADA.value:
            raise RegraDeNegocioError("Esta prescrição já foi administrada ao paciente e não pode ser cancelada.")
            
        if prescricao.status == StatusPrescricao.CANCELADA.value:
            raise RegraDeNegocioError("Esta prescrição já se encontra cancelada.")

        prescricao.status = StatusPrescricao.CANCELADA.value
        self.prescricao_repo.atualizar_prescricao(prescricao)

   

    def aplicar_medicamento(self, id_prescricao: int, enfermeiro_id: int) -> Prescricao:
        """
        Ação exclusiva da Enfermagem após administrar a medicação física no paciente.
        """
        prescricao = self.buscar_prescricao_valida(id_prescricao)

        
        if prescricao.status == StatusPrescricao.APLICADA.value:
            raise RegraDeNegocioError("Cuidado: Dose duplicada! Esta medicação já consta como aplicada.")
            
        if prescricao.status == StatusPrescricao.CANCELADA.value:
            raise RegraDeNegocioError("O médico suspendeu/cancelou esta prescrição. Não administre ao paciente!")
        
        prescricao.status = StatusPrescricao.APLICADA.value
        prescricao.enfermeiro_id = enfermeiro_id
        prescricao.data_hora_aplicacao = datetime.now() 

        self.prescricao_repo.atualizar_prescricao(prescricao)
        
        return prescricao


    def ver_detalhes_aplicacao(self, id_prescricao: int) -> Prescricao:
       
        prescricao = self.prescricao_repo.buscar_precricao_enfermeiro(id_prescricao)
        
        if not prescricao:
            raise NaoEncontradoError("Prescrição médica não encontrada.")
            
        return prescricao