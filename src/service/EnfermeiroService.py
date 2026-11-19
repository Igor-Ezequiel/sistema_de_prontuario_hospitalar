from src.models.Classes import Enfermeiro
from src.repositori.Equipe_Medica.EnfermeiroRepository import EnfermeiroRepository
from src.security import gerar_hash_senha
from src.exceptions import NaoEncontradoError, RegraDeNegocioError

class EnfermeiroService:
    def __init__(self, enfermeiro_repo: EnfermeiroRepository):
        self.enfermeiro_repo = enfermeiro_repo

    def cadastrar_enfermeiro(self, nome: str, coren: str, email: str, senha_plana: str) -> int:
      
        coren_em_uso = self.enfermeiro_repo.buscar_por_coren(coren)
        if coren_em_uso:
            raise RegraDeNegocioError("Já existe um enfermeiro cadastrado com este COREN.")

       
        senha_protegida = gerar_hash_senha(senha_plana)

        
        novo_enfermeiro = Enfermeiro(
            id_enfermeiro=None, 
            nome=nome,
            coren=coren,
            email=email,
            senha=senha_protegida,
            ativo=True       
        )
        
       
        return self.enfermeiro_repo.inserir_enfermeiro(novo_enfermeiro)

    def buscar_enfermeiro_valido(self, id_enfermeiro: int) -> Enfermeiro:
       
        enfermeiro = self.enfermeiro_repo.buscar_por_id(id_enfermeiro)
        
        if not enfermeiro:
            raise NaoEncontradoError("Enfermeiro não encontrado no sistema.")
            
        if not enfermeiro.ativo:
            raise RegraDeNegocioError("Este enfermeiro está inativo e sem acesso ao sistema.")
            
        return enfermeiro

    def atualizar_dados(self, id_enfermeiro: int, nome: str, coren: str) -> Enfermeiro:
        
        enfermeiro = self.buscar_enfermeiro_valido(id_enfermeiro)
                
       
        if enfermeiro.coren != coren:
            coren_em_uso = self.enfermeiro_repo.buscar_por_coren(coren)
            if coren_em_uso:
                raise RegraDeNegocioError("O novo COREN informado já pertence a outro profissional.")
                
        
        enfermeiro.nome = nome
        enfermeiro.coren = coren
            
       
        self.enfermeiro_repo.atualizar_enfermeiro(enfermeiro)
        
        return enfermeiro

    def inativar_enfermeiro(self, id_enfermeiro: int):
        
        self.buscar_enfermeiro_valido(id_enfermeiro)
        
       
        self.enfermeiro_repo.desativar_enfermeiro(id_enfermeiro)