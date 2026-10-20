
class Paciente:
    def __init__(self, id_paciente, nome, cpf, data_nascimento):
        self.id = id_paciente
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Medico:
    def __init__(self, id_medico, nome, crm):
        self.id = id_medico
        self.nome = nome
        self.crm = crm

class Triagem:
    
    def __init__(self, id_triagem, pressao, temperatura, saturacao, data_hora):
        self.id = id_triagem
        self.pressao = pressao
        self.temperatura = temperatura
        self.saturacao = saturacao
        self.data_hora = data_hora

class Cid:
    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

class Prescricao:
    def __init__(self, id_prescricao, nome_remedio, dose, intervalo_horas, status):
        self.id = id_prescricao
        self.nome_remedio = nome_remedio 
        self.dose = dose
        self.intervalo_horas = intervalo_horas
        self.status = status


class Evolucao:
    def __init__(self, id_evolucao, relato, dias_entubacao, data_hora, medico_autor):
        self.id = id_evolucao
        self.relato = relato
        self.dias_entubacao = dias_entubacao
        self.data_hora = data_hora
        self.medico_autor = medico_autor
        
        self.diagnosticos = []    
        self.prescricoes = [] 



class Prontuario:
    def __init__(self, atendimento_id, status, cor_risco, data_entrada, data_alta):
        self.id = atendimento_id
        self.status = status
        self.cor_risco = cor_risco
        self.data_entrada = data_entrada
        self.data_alta = data_alta
        
        self.paciente = None       
        self.medico = None 
        
        self.triagens = [] 
        self.evolucoes = []


