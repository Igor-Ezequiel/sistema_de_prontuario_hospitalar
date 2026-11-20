from enum import Enum


def _limpar_cpf(cpf: str | None) -> str | None:
    if cpf is None:
        return None
    return "".join(filter(str.isdigit, cpf))


class StatusAtendimento(str, Enum):
    AGUARDANDO_TRIAGEM = "Aguardando Triagem"
    AGUARDANDO_MEDICO = "Aguardando Médico"
    EM_ATENDIMENTO = "Em Atendimento"
    ALTA = "Alta"
    CANCELADO = "Cancelado"


class CorRisco(str, Enum):
    VERMELHO = "Vermelho"
    LARANJA = "Laranja"
    AMARELO = "Amarelo"
    VERDE = "Verde"
    AZUL = "Azul"
    CINZA = "Cinza"

    def DefinirPeso(self) -> int:
        match self.value:
            case "Vermelho": return 9
            case "Laranja": return 8
            case "Amarelo": return 7
            case "Verde": return 6
            case "Azul": return 5
            case _: return 0


class StatusPrescricao(str, Enum):
    PENDENTE = "Pendente"
    APLICADA = "Aplicada"
    CANCELADA = "Cancelada"


class Usuario:
    def __init__(
        self,
        id_usuario: int,
        email: str,
        senha: str,
        cargo: str,
        ativo: bool = True,
        cpf: str = None,
    ):
        self.id = id_usuario
        self.email = email
        self.senha = senha
        self.cargo = cargo
        self.ativo = ativo
        self.cpf = _limpar_cpf(cpf)


class Coordenador(Usuario):
    def __init__(
        self,
        id_coordenador: int,
        nome: str,
        setor_responsavel: str,
        email: str = None,
        senha: str = None,
        ativo: bool = True,
        cpf: str = None,
    ):
        super().__init__(
            id_coordenador,
            email,
            senha,
            cargo="Coordenador",
            ativo=ativo,
            cpf=cpf,
        )
        self.nome = nome
        self.setor_responsavel = setor_responsavel


class Enfermeiro(Usuario):
    def __init__(
        self,
        id_enfermeiro: int,
        nome: str,
        coren: str,
        email: str = None,
        senha: str = None,
        ativo: bool = True,
        cpf: str = None,
    ):
        super().__init__(
            id_enfermeiro,
            email,
            senha,
            cargo="Enfermeiro",
            ativo=ativo,
            cpf=cpf,
        )
        self.nome = nome
        self.coren = coren


class Medico(Usuario):
    def __init__(
        self,
        id_medico: int,
        nome: str,
        crm: str,
        especialidade: str = None,
        email: str = None,
        senha: str = None,
        ativo: bool = True,
        cpf: str = None,
    ):
        super().__init__(
            id_medico,
            email,
            senha,
            cargo="Medico",
            ativo=ativo,
            cpf=cpf,
        )
        self.nome = nome
        self.crm = crm
        self.especialidade = especialidade


class Paciente:
    def __init__(
        self,
        id_paciente: int,
        nome: str,
        cpf: str,
        data_nascimento,
        usuario_id: int = None,
        ativo: bool = True,
    ):
        self.id = id_paciente
        self.nome = nome
        self.cpf = _limpar_cpf(cpf)
        self.data_nascimento = data_nascimento
        self.usuario_id = usuario_id

        self.ativo = ativo
        self.usuario = None


class Plantao:
    def __init__(
        self,
        id_plantao: int,
        setor_ala: str,
        data_hora_inicio,
        data_hora_fim,
        medico_id: int,
        coordenador_id: int,
    ):
        self.id = id_plantao
        self.setor_ala = setor_ala
        self.data_hora_inicio = data_hora_inicio
        self.data_hora_fim = data_hora_fim
        self.medico_id = medico_id
        self.coordenador_id = coordenador_id

        self.medico = None
        self.coordenador = None


class Triagem:
    def __init__(
        self,
        id_triagem: int,
        pressao: str,
        temperatura: float,
        saturacao: int,
        data_hora,
        atendimento_id: int = None,
        enfermeiro_id: int = None,
    ):
        self.id = id_triagem
        self.pressao = pressao
        self.temperatura = temperatura
        self.saturacao = saturacao
        self.data_hora = data_hora
        self.atendimento_id = atendimento_id
        self.enfermeiro_id = enfermeiro_id
        self.enfermeiro = None


class Prescricao:
    def __init__(
        self,
        id_prescricao: int,
        nome_medicamento: str,
        dose: str,
        intervalo_horas: int,
        status: str,
        evolucao_id: int = None,
        enfermeiro_id: int = None,
        data_hora_aplicacao=None,
    ):
        self.id = id_prescricao
        self.nome_medicamento = nome_medicamento
        self.dose = dose
        self.intervalo_horas = intervalo_horas
        self.status = status
        self.evolucao_id = evolucao_id
        self.enfermeiro_id = enfermeiro_id
        self.data_hora_aplicacao = data_hora_aplicacao

        self.enfermeiro = None


class Evolucao:
    def __init__(
        self,
        id_evolucao: int,
        relato: str,
        data_hora,
        dias_entubacao: int = None,
        atendimento_id: int = None,
        medico_id: int = None,
        medico_autor: str = None,
    ):
        self.id = id_evolucao
        self.relato = relato
        self.dias_entubacao = dias_entubacao
        self.data_hora = data_hora
        self.atendimento_id = atendimento_id
        self.medico_id = medico_id
        self.medico_autor = medico_autor

        self.diagnosticos = []
        self.prescricoes = []


class CID:
    def __init__(self, codigo: str, descricao: str):
        self.codigo = codigo
        self.descricao = descricao


class Atendimento:
    def __init__(
        self,
        atendimento_id: int,
        status: StatusAtendimento,
        cor_risco: CorRisco,
        data_entrada,
        paciente_id: int,
        data_alta=None,
        medico_id: int = None,
    ):
        self.id = atendimento_id
        self.status = status
        self.cor_risco = cor_risco
        self.data_entrada = data_entrada
        self.paciente_id = paciente_id
        self.data_alta = data_alta
        self.medico_id = medico_id

        self.paciente = None
        self.medico = None
        self.triagens = []
        self.evolucoes = []
        self.permissoes_extras = []