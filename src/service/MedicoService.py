from datetime import datetime
from src.models.Classes import Medico
from src.repositori.Equipe_Medica.MedicoRepository import MedicoRepository
from src.security import gerar_hash_senha
from src.exceptions import NaoEncontradoError, RegraDeNegocioError

class MedicoService:
    def __init__(self, medico_repo: MedicoRepository):
        self.medico_repo = medico_repo

    def cadastrar_medico(self, nome: str, crm: str, especialidade: str, email: str, senha_plana: str) -> int:
        
        crm_em_uso = self.medico_repo.buscar_por_crm(crm)
        if crm_em_uso:
            raise RegraDeNegocioError("Já existe um médico cadastrado com este CRM no hospital.")

        
        senha_protegida = gerar_hash_senha(senha_plana)

      
        novo_medico = Medico(
            id_medico=None, 
            nome=nome,
            crm=crm,
            especialidade=especialidade,
            email=email,
            senha=senha_protegida,
            ativo=True       
        )
        
       
        return self.medico_repo.inserir_medico(novo_medico)

    def buscar_medico_valido(self, id_medico: int) -> Medico:
       
        medico = self.medico_repo.buscar_por_id(id_medico)
        
        if not medico:
            raise NaoEncontradoError("Médico não encontrado no sistema.")
            
        if not medico.ativo:
            raise RegraDeNegocioError("Este médico está inativo e sem acesso ao sistema.")
            
        return medico

    def atualizar_dados(self, id_medico: int, nome: str, crm: str, especialidade: str) -> Medico:
       
        medico = self.buscar_medico_valido(id_medico)
                
        
        if medico.crm != crm:
            crm_em_uso = self.medico_repo.buscar_por_crm(crm)
            if crm_em_uso:
                raise RegraDeNegocioError("O novo CRM informado já pertence a outro profissional.")
                
       
        medico.nome = nome
        medico.crm = crm
        medico.especialidade = especialidade
            
       
        self.medico_repo.atualizar_medico(medico)
        
        return medico

    def inativar_medico(self, id_medico: int):
        
        self.buscar_medico_valido(id_medico)
        
      
        self.medico_repo.desativar_medico(id_medico)


    def buscar_medicos_para_plantao(self, inicio_desejado: datetime, fim_desejado: datetime) -> list[Medico]:
       
        if inicio_desejado >= fim_desejado:
            raise RegraDeNegocioError("A data/hora de início do plantão deve ser anterior à data de fim do plantao.")
            
       
        return self.medico_repo.buscar_medicos_disponiveis(inicio_desejado, fim_desejado)