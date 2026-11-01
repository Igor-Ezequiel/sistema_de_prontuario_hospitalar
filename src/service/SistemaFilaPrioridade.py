from src.models import CorRisco 
from queue import PriorityQueue
from datetime import datetime

class FichaAtendimento:
    def __init__(self, id_atendimento: int, data_entrada: datetime, corrisco: CorRisco):
        self.id = id_atendimento
        self.data = data_entrada
        self.corrisco = corrisco

class Fila_Prioridade:
    
    def __init__(self, limite_pacientes=500):
        self.fila = PriorityQueue(maxsize=limite_pacientes)
        
    def Inserir_Paciente(self, ficha: FichaAtendimento):
        
        if self.Verificar_QuantidadeMax(): 
            print("Fila cheia!")
            return None
            
        peso = -ficha.corrisco.DefinirPeso()
        tupla = (peso, ficha.data, ficha)
        
        self.fila.put_nowait(tupla)
        print(f"[ENTRADA] Paciente da Ficha #{ficha.id} ({ficha.corrisco.value}) entrou na fila.")
        
    def Atender_Proximo_Paciente(self):
    
        if self.Verificar_Estado_Fila(): 
            print("Nenhum chamado pendente!")
            return None
        
        peso, data, ficha = self.fila.get_nowait()
        
        
        print(
            f"-> [ATENDENDO] Chamado #{ficha.id} "
            f"(Severidade: {ficha.corrisco.value} | Chegada em: {data})"
        )
        
        
        return ficha 
        
    def Verificar_Tamanho(self):
        return self.fila.qsize()
    
    def Verificar_Estado_Fila(self):
        
        return self.fila.empty()
    
    def Verificar_QuantidadeMax(self):
        
        return self.fila.full()
    
    
fila_hospital = Fila_Prioridade()