from src.repositori.Equipe_Medica.UsuarioRepository import UsuarioRepository
from src.models.Classes import Usuario
from src.security import gerar_hash_senha, verificar_senha
from src.exceptions import (
    NaoEncontradoError, 
    RegraDeNegocioError, 
    PermissaoNegadaError
)

class UsuarioService:
    
    def __init__(self, usuario_repositorio: UsuarioRepository):
        self.repositori_usuario = usuario_repositorio

    def fazer_login(self, email: str, senha: str) -> Usuario:
        
        usuario = self.repositori_usuario.buscar_por_email(email)
        
        if not usuario:
            raise PermissaoNegadaError("E-mail ou senha incorretos!")
        
        if not usuario.ativo:
            raise PermissaoNegadaError("Usuário está inativo no sistema!")
        
        if not verificar_senha(senha, usuario.senha):
            raise PermissaoNegadaError("E-mail ou senha incorretos!")
        
        return usuario

    def Criar_Usuario(self, email: str, senha: str, cargo: str, ativo: bool = True) -> int:
        
        if self.repositori_usuario.buscar_por_email(email):
            raise RegraDeNegocioError("Este e-mail já está cadastrado.")

        senha_hash = gerar_hash_senha(senha)

        novo_usuario = Usuario(
            id_usuario=None,
            email=email,
            senha=senha_hash,
            cargo=cargo,
            ativo=ativo
        )
        return self.repositori_usuario.inserir_usuario(novo_usuario)
    
    def Buscar_Usuario(self, id_usuario: int) -> Usuario:
      
        usuario = self.repositori_usuario.buscar_por_id(id_usuario)
        
        if not usuario:
            raise NaoEncontradoError("Usuário não encontrado.")
            
        return usuario

    def Atualizar_Credenciais(self, id_usuario: int, email: str, senha: str = None):
        
        usuario = self.Buscar_Usuario(id_usuario)

        if email != usuario.email:
            email_em_uso = self.repositori_usuario.buscar_por_email(email)
            if email_em_uso:
                raise RegraDeNegocioError("Este e-mail já está sendo usado por outro usuário.")
            usuario.email = email

        if senha:
            usuario.senha = gerar_hash_senha(senha)
            
        self.repositori_usuario.atualizar_usuario(usuario)


    def Desativar_Usuario(self, id_usuario: int):
        
        usuario = self.Buscar_Usuario(id_usuario)
        
        if not usuario.ativo:
            raise RegraDeNegocioError("Este usuário já está inativo no sistema.")
            
        self.repositori_usuario.desativar_usuario(id_usuario)


    def Reativar_Usuario(self, id_usuario: int):
        
        usuario = self.Buscar_Usuario(id_usuario)
        
        if usuario.ativo:
            raise RegraDeNegocioError("Este usuário já está ativo no sistema.")
            
        self.repositori_usuario.reativar_usuario(id_usuario)
        
       
        