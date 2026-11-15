from src.repositori.Equipe_Medica.UsuarioRepositori import UsuarioRepositori
from src.models.Classes import Usuario
from src.security import gerar_hash_senha, verificar_senha
from src.exceptions import (
    NaoEncontradoError, 
    RegraDeNegocioError, 
    PermissaoNegadaError
)

class UsuarioService:
    
    def __init__(self, usuario_repositorio: UsuarioRepositori):
        self.repositori_usuario = usuario_repositorio

    def fazer_login(self, email: str, senha_digitada: str) -> Usuario:
        usuario = self.repositori_usuario.buscar_por_email(email)
        
        if not usuario:
            raise PermissaoNegadaError("E-mail ou senha incorretos!")
        
        if not usuario.ativo:
            raise PermissaoNegadaError("Usuário está inativo no sistema!")
        
        if not verificar_senha(senha_digitada, usuario.senha):
            raise PermissaoNegadaError("E-mail ou senha incorretos!")
        
        return usuario

    def Criar_Usuario(self, email: str, senha_plana: str, cargo: str, ativo: bool = True) -> int:
        
        if self.repositori_usuario.buscar_por_email(email):
            raise RegraDeNegocioError("Este e-mail já está cadastrado.")

        senha_hash = gerar_hash_senha(senha_plana)

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

    def Atualizar_Credenciais(self, id_usuario: int, novo_email: str, nova_senha_plana: str = None):
        
        usuario = self.Buscar_Usuario(id_usuario)

        if novo_email != usuario.email:
            email_em_uso = self.repositori_usuario.buscar_por_email(novo_email)
            if email_em_uso:
                raise RegraDeNegocioError("Este e-mail já está sendo usado por outro usuário.")
            usuario.email = novo_email

        if nova_senha_plana:
            usuario.senha = gerar_hash_senha(nova_senha_plana)
            
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
        
       
        