from src.models.Classes import Coordenador
from src.repositori.Equipe_Medica.CoordenadorRepository import CoordenadorRepository
from src.security import gerar_hash_senha
from src.exceptions import NaoEncontradoError, RegraDeNegocioError

class CoordenadorService:
    def __init__(self, coordenador_repo: CoordenadorRepository):
        self.coordenador_repo = coordenador_repo

    def cadastrar_coordenador(self, nome: str, setor_responsavel: str, email: str, senha_plana: str) -> int:
       
        senha_protegida = gerar_hash_senha(senha_plana)

        
        novo_coordenador = Coordenador(
            id_coordenador=None, 
            nome=nome,
            setor_responsavel=setor_responsavel,
            email=email,
            senha=senha_protegida,
            ativo=True       
        )
        
       
        return self.coordenador_repo.inserir_coordenador(novo_coordenador)

    def buscar_coordenador_valido(self, id_coordenador: int) -> Coordenador:
       
        coordenador = self.coordenador_repo.buscar_por_id(id_coordenador)
        
        if not coordenador:
            raise NaoEncontradoError("Coordenador não encontrado no sistema.")
            
        if not coordenador.ativo:
            raise RegraDeNegocioError("Este coordenador está inativo e sem acesso ao sistema.")
            
        return coordenador

    def atualizar_dados(self, id_coordenador: int, nome: str, setor_responsavel: str) -> Coordenador:
       
        coordenador = self.buscar_coordenador_valido(id_coordenador)
                
       
        coordenador.nome = nome
        coordenador.setor_responsavel = setor_responsavel
            
       
        self.coordenador_repo.atualizar_coordenador(coordenador)
        
        return coordenador

    def inativar_coordenador(self, id_coordenador: int):
       
        self.buscar_coordenador_valido(id_coordenador)
        
       
        self.coordenador_repo.desativar_coordenador(id_coordenador)