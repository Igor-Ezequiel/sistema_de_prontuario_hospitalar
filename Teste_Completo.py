from collections import namedtuple
from datetime import datetime
import sqlite3
import time

from src.models.Classes import CorRisco, StatusAtendimento
from src.repositori.AtendimentoRepositori import AtendimentoRepository
from src.repositori.TriagemRepositori import TriagemRepository
from src.service.AtendimentoService import AtendimentoService
from src.service.SistemaFilaPrioridade import fila_hospital
from src.service.TriagemService import TriagemService


# ==============================================================================
# 1. BANCO EM MEMÓRIA PARA RODAR O SEU SQL REAL (JOINs, INSERTs, UPDATEs)
# ==============================================================================
class ConexaoBancoTeste:

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = lambda cursor, row: namedtuple(
            "Row", [col[0] for col in cursor.description]
        )(*row)
        self._criar_tabelas_e_dados_base()

    def _criar_tabelas_e_dados_base(self):
        queries = [
            "CREATE TABLE paciente (id INTEGER PRIMARY KEY, nome TEXT, cpf TEXT, data_nascimento TEXT)",
            "CREATE TABLE medico (id INTEGER PRIMARY KEY, nome TEXT, crm TEXT)",
            "CREATE TABLE atendimento (id INTEGER PRIMARY KEY AUTOINCREMENT, data_hora_entrada TIMESTAMP, data_hora_alta TIMESTAMP, status TEXT, cor_risco TEXT, paciente_id INTEGER, medico_id INTEGER)",
            "CREATE TABLE triagem (id INTEGER PRIMARY KEY AUTOINCREMENT, pressao_arterial TEXT, temperatura REAL, saturacao INTEGER, data_hora TIMESTAMP, atendimento_id INTEGER, enfermeiro_id INTEGER)",
            "CREATE TABLE evolucao_clinica (id INTEGER PRIMARY KEY AUTOINCREMENT, relato_clinico_observacoes TEXT, dias_entubacao INTEGER, data_hora TIMESTAMP, atendimento_id INTEGER, medico_id INTEGER)",
            "INSERT INTO paciente VALUES (1, 'Carlos Silva', '111.111.111-11', '1985-05-10')",
            "INSERT INTO paciente VALUES (2, 'Ana Souza', '222.222.222-22', '1992-08-22')",
            "INSERT INTO paciente VALUES (3, 'Roberto Gomes', '333.333.333-33', '1970-01-15')",
            "INSERT INTO medico VALUES (10, 'Dr. Gregory House', 'CRM-RJ 12345')",
        ]
        for q in queries:
            self.conn.execute(q)
        self.conn.commit()

    def execute(self, sql, params=None):
        return self.conn.execute(sql, params or {})

    def commit(self):
        self.conn.commit()


# ==============================================================================
# 2. INSTANCIANDO REPOSITÓRIOS E SERVICES
# ==============================================================================
db_teste = ConexaoBancoTeste()
atendimento_repo = AtendimentoRepository(db_teste)
triagem_repo = TriagemRepository(db_teste)

atendimento_service = AtendimentoService(atendimento_repo)
triagem_service = TriagemService(triagem_repo, atendimento_repo)

print("=" * 60)
print("ETAPA 1: RECEPÇÃO (CRIANDO ATENDIMENTOS)")
print("=" * 60)
atend_carlos = atendimento_service.criar_atendimento(paciente_id=1)
time.sleep(0.05)
atend_ana = atendimento_service.criar_atendimento(paciente_id=2)
time.sleep(0.05)
atend_roberto = atendimento_service.criar_atendimento(paciente_id=3)
print(
    f"Fichas abertas com sucesso! IDs gerados: {atend_carlos}, {atend_ana}, {atend_roberto}\n"
)


print("=" * 60)
print("ETAPA 2: TRIAGEM, CORREÇÃO DE ERRO E EMERGÊNCIA")
print("=" * 60)
# 1. Carlos passa pela triagem -> VERDE (Pouco urgente)
triagem_service.Criar_triagem(
    atendimento_id=atend_carlos,
    enfermeiro_id=50,
    pressao="120/80",
    temperatura=36.8,
    saturacao=98,
    nova_cor=CorRisco.VERDE,
)

# Simulando enfermeiro errando uma aferição extra do Carlos, corrigindo e depois excluindo
id_triagem_errada = triagem_repo.inserir_triagem(
    triagem_service.buscar_triagens(atend_carlos)[0]
)
triagem_service.corrigir_erro_afericao(
    id_triagem_errada,
    nova_pressao="125/85",
    nova_temperatura=37.0,
    nova_saturacao=99,
)
triagem_service.deletar_triagem_invalida(id_triagem_errada)

# 2. Ana passa pela triagem -> LARANJA (Muita urgência)
triagem_service.Criar_triagem(
    atendimento_id=atend_ana,
    enfermeiro_id=50,
    pressao="160/100",
    temperatura=39.2,
    saturacao=91,
    nova_cor=CorRisco.LARANJA,
)

# 3. Roberto chega em estado grave -> VERMELHO direto pelo AtendimentoService!
atendimento_service.Classificar_Risco(
    atendimento_id=atend_roberto, nova_cor=CorRisco.VERMELHO
)


print("\n" + "=" * 60)
print("ETAPA 3: TESTANDO A FILA DE PRIORIDADE (ORDEM DE CHAMADA)")
print("=" * 60)
print(
    f"Pacientes aguardando na fila: {fila_hospital.Verificar_Tamanho()} (Esperado: Roberto -> Ana -> Carlos)\n"
)

while not fila_hospital.Verificar_Estado_Fila():
    ficha_chamada = fila_hospital.Atender_Proximo_Paciente()


print("\n" + "=" * 60)
print("ETAPA 4: EVOLUÇÃO, ALTA E BUSCA DO PRONTUÁRIO COMPLETO")
print("=" * 60)
ficha_ana = atendimento_service.buscar_atendimento(atend_ana)
ficha_ana.medico_id = 10
atendimento_repo.atualizar_dados_atendimento(ficha_ana)

db_teste.execute(
    """
    INSERT INTO evolucao_clinica (relato_clinico_observacoes, dias_entubacao, data_hora, atendimento_id, medico_id)
    VALUES ('Paciente medicada com antitérmico intravenoso. Quadro estabilizado.', 0, :agora, :atend_id, 10)
    """,
    {"agora": datetime.now(), "atend_id": atend_ana},
)
db_teste.commit()

atendimento_service.dar_alta(atend_ana)

prontuario_ana = atendimento_repo.buscar_prontuario(atend_ana)

print(f"PRONTUÁRIO DA FICHA #{prontuario_ana.id}")
print(
    f"Paciente: {prontuario_ana.paciente.nome} (CPF: {prontuario_ana.paciente.cpf})"
)
print(
    f"Médico Responsável: {prontuario_ana.medico.nome} ({prontuario_ana.medico.crm})"
)
print(
    f"Status Atual: {prontuario_ana.status} | Risco: {prontuario_ana.cor_risco}"
)
print(
    f"Data Entrada: {prontuario_ana.data_entrada} | Data Alta: {prontuario_ana.data_alta}"
)

print("\n-> Histórico de Triagens no Prontuário:")
for t in prontuario_ana.triagens:
    print(
        f"   [Triagem #{t.id}] PA: {t.pressao} | Temp: {t.temperatura}ºC | Sat: {t.saturacao}%"
    )

print("\n-> Histórico de Evoluções Clínicas no Prontuário:")
for ev in prontuario_ana.evolucoes:
    print(
        f"   [Evolução #{ev.id} - {ev.medico_autor}]: {ev.relato} (Intubação: {ev.dias_entubacao} dias)"
    )