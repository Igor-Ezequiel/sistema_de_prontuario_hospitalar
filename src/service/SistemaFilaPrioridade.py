from queue import PriorityQueue
from src.models.Classes import Atendimento
from src.exceptions import RegraDeNegocioError

class Fila_Prioridade:

    def __init__(self, limite_pacientes=500):
        self.fila = PriorityQueue(maxsize=limite_pacientes)

    def Inserir_Paciente(self, ficha: Atendimento):
        
        if self.Verificar_QuantidadeMax():
            
            raise RegraDeNegocioError("A fila de prioridade do hospital atingiu a capacidade máxima!")

        peso = -ficha.cor_risco.DefinirPeso()
        tupla = (peso, ficha.data_entrada, ficha)

        self.fila.put_nowait(tupla)
        
        
        print(f"[ENTRADA FILA] Paciente da Ficha #{ficha.id} ({ficha.cor_risco.value}) entrou na fila.")

    def Atender_Proximo_Paciente(self) -> Atendimento:
        
        if self.Verificar_Estado_Fila():
            
            raise RegraDeNegocioError("Nenhum paciente aguardando na fila no momento!")

        peso, data, ficha = self.fila.get_nowait()

        print(
            f"-> [CHAMANDO NO PAINEL] Ficha #{ficha.id} "
            f"(Severidade: {ficha.cor_risco} | Chegada em: {data})"
        )
        
        return ficha
    
    def Verificar_Tamanho(self):
        return self.fila.qsize()

    def Verificar_Estado_Fila(self):
        return self.fila.empty()

    def Verificar_QuantidadeMax(self):
        return self.fila.full()


fila_hospital = Fila_Prioridade()