# Caminho: pasta src -> pasta models -> arquivo Classes.py
from src.models.Classes import (
    StatusAtendimento, 
    CorRisco, 
    Atendimento, 
    Triagem, 
    Evolucao,
    Paciente
)

# Caminho: pasta src -> pasta repositori -> arquivo ProntuarioRepositori.py
from src.repositori.ProntuarioRepositori import AtendimentoRepository

# 2. Renomeie a classe para Service para não misturar as camadas
class AtendimentoService:
    
    def __init__(self, repositori: AtendimentoRepository):
        self.repositori = repositori
        
    def CriarProntuario(self, atendimento_id: int):
        
        # Agora, ao digitar o ponto, funções como 'buscar_simples_por_id' vão aparecer!
        criar = self.repositori
