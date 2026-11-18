from src.models.Classes import Paciente
from repositori.Equipe_Medica.PacienteRepository import PacienteRepositori
from repositori.Equipe_Medica.UsuarioRepository import UsuarioRepositori
from src.exceptions import NaoEncontradoError, RegraDeNegocioError

class PacienteService:
    def __init__(self, paciente_repo: PacienteRepositori, usuario_repo: UsuarioRepositori):
        self.repositorio_paciente = paciente_repo
        self.repositorio_usuario = usuario_repo

    def cadastrar_paciente(self, nome: str, cpf: str, data_nascimento) -> int:
        paciente_existente = self.repositorio_paciente.buscar_por_cpf(cpf)
        
        if paciente_existente:
            raise RegraDeNegocioError('O CPF já está cadastrado!')
        
        usuario_existente = self.repositorio_usuario.buscar_por_cpf(cpf)
        
        if usuario_existente:
            id_vinculado = usuario_existente.id_usuario
        else:
            id_vinculado = None
            
        novo_paciente = Paciente(
            id_paciente=None, 
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nascimento,
            usuario_id=id_vinculado,
            ativo=True       
        )
        
        return self.repositorio_paciente.inserir_paciente(novo_paciente)


    def buscar_paciente_valido(self, id_paciente: int) -> Paciente:
        
        paciente = self.repositorio_paciente.buscar_por_id(id_paciente)
        
        if not paciente:
            raise NaoEncontradoError("Paciente não encontrado no sistema.")
            
        if not paciente.ativo:
            raise RegraDeNegocioError("Este paciente está inativo (excluído) e não pode receber novos atendimentos.")
            
        return paciente


    def atualizar_dados(self, id_paciente: int, nome: str, cpf: str, data_nascimento, usuario_id: int = None) -> Paciente:
       
        paciente = self.buscar_paciente_valido(id_paciente)
        
        if paciente.cpf != cpf:
            cpf_em_uso = self.repositorio_paciente.buscar_por_cpf(cpf)
            if cpf_em_uso:
                raise RegraDeNegocioError("O novo CPF informado já pertence a outro paciente cadastrado.")
                
        paciente.nome = nome
        paciente.cpf = cpf
        paciente.data_nascimento = data_nascimento
        
        if usuario_id is not None:
            paciente.usuario_id = usuario_id
            
        self.repositorio_paciente.atualizar_paciente(paciente)
        
        return paciente


    def inativar_paciente(self, id_paciente: int):
    
        paciente = self.buscar_paciente_valido(id_paciente)
        
        self.repositorio_paciente.excluir_paciente(id_paciente)