import sqlite3
import heapq
from types import SimpleNamespace

from src.models.Classes import (
    Atendimento,
    Paciente,
    Medico,
    Enfermeiro,
    Triagem,
    Evolucao,
    CID,
    StatusAtendimento,
    CorRisco
)
from repositori.AtendimentoRepository import AtendimentoRepository
from repositori.TriagemRepository import TriagemRepository
from repositori.EvolucaoRepository import EvolucaoRepositori


# --- ADAPTADOR DE BANCO EM MEMÓRIA ---
class BancoDeTeste:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = lambda cursor, row: SimpleNamespace(
            **{col[0]: row[idx] for idx, col in enumerate(cursor.description)}
        )

    def execute(self, sql: str, params: dict = None):
        if params is None:
            return self.conn.execute(sql)
        return self.conn.execute(sql, params)

    def commit(self):
        self.conn.commit()


# --- ESTRUTURA DA FILA DE PRIORIDADE (PROTOCOLO DE MANCHESTER) ---
class FilaManchester:
    PESOS = {
        "VERMELHO": 1,
        "LARANJA": 2,
        "AMARELO": 3,
        "VERDE": 4,
        "AZUL": 5
    }

    def __init__(self):
        self._fila = []
        self._ordem_chegada = 0

    def adicionar_paciente(self, atendimento: Atendimento, nome_paciente: str, hora_triagem: str):
        cor_str = atendimento.cor_risco.name if hasattr(atendimento.cor_risco, "name") else str(atendimento.cor_risco)
        peso = self.PESOS.get(cor_str.upper(), 5)
        self._ordem_chegada += 1
        heapq.heappush(self._fila, (peso, self._ordem_chegada, nome_paciente, hora_triagem, atendimento))

    def chamar_proximo(self) -> tuple[str, Atendimento]:
        if not self._fila:
            return None, None
        peso, ordem, nome, hora, atendimento = heapq.heappop(self._fila)
        return nome, atendimento

    def exibir_painel_fila(self):
        print("\n  +---------------------------------------------------------------------+")
        print("  | PAINEL DA FILA DE ESPERA (ORDENADA POR PRIORIDADE DE MANCHESTER)    |")
        print("  +---------------------------------------------------------------------+")
        if not self._fila:
            print("  | [Fila vazia no momento]                                             |")
        else:
            # Faz uma cópia ordenada apenas para exibir a fila sem remover os pacientes
            fila_ordenada = sorted(self._fila)
            for pos, (peso, ordem, nome, hora, atend) in enumerate(fila_ordenada, start=1):
                print(f"  | {pos}º da Fila -> {nome:<15} | Risco: {atend.cor_risco:<8} | Triado às: {hora} |")
        print("  +---------------------------------------------------------------------+")


# --- FUNÇÃO PARA EXIBIR 100% DOS DADOS DO PRONTUÁRIO (SEM RESUMOS) ---
def imprimir_prontuario_completo(prontuario: Atendimento, titulo_momento: str):
    print("\n" + "=" * 75)
    print(f"PRONTUÁRIO MÉDICO COMPLETO ({titulo_momento})")
    print("=" * 75)

    print("[DADOS DO ATENDIMENTO]")
    print(f"  ID do Atendimento : #{prontuario.id}")
    print(f"  Status Atual      : {prontuario.status}")
    print(f"  Classif. de Risco : {prontuario.cor_risco}")
    print(f"  Data/Hora Entrada : {prontuario.data_entrada}")
    print(f"  Data/Hora Alta    : {prontuario.data_alta if prontuario.data_alta else 'Em aberto (Paciente em atendimento)'}")
    print(f"  ID Paciente (FK)  : {prontuario.paciente_id}")
    print(f"  ID Médico (FK)    : {prontuario.medico_id if prontuario.medico_id else 'Ainda não vinculado'}")

    print("\n[DADOS DO PACIENTE]")
    if prontuario.paciente:
        print(f"  ID do Paciente    : #{prontuario.paciente.id}")
        print(f"  Nome Completo     : {prontuario.paciente.nome}")
        print(f"  CPF               : {prontuario.paciente.cpf}")
        print(f"  Data de Nascimento: {prontuario.paciente.data_nascimento}")

    print("\n[MÉDICO RESPONSÁVEL PELO ATENDIMENTO / ALTA]")
    if prontuario.medico:
        print(f"  ID do Médico      : #{prontuario.medico.id}")
        print(f"  Nome do Médico    : {prontuario.medico.nome}")
        print(f"  CRM               : {prontuario.medico.crm}")
    else:
        print("  Nenhum médico vinculado à alta até o momento.")

    print(f"\n[HISTÓRICO COMPLETO DE TRIAGENS] (Total: {len(prontuario.triagens)})")
    if not prontuario.triagens:
        print("  Nenhuma triagem registrada.")
    else:
        for idx, t in enumerate(prontuario.triagens, start=1):
            print(f"  --- Triagem {idx} (ID Triagem: #{t.id} | Atendimento FK: #{t.atendimento_id}) ---")
            print(f"      Data/Hora         : {t.data_hora}")
            print(f"      Pressão Arterial  : {t.pressao} mmHg")
            print(f"      Temperatura       : {t.temperatura} °C")
            print(f"      Saturação (SpO2)  : {t.saturacao}%")
            if t.enfermeiro:
                print(f"      Enfermeiro Resp.  : [ID #{t.enfermeiro.id}] {t.enfermeiro.nome} (COREN: {t.enfermeiro.coren})")

    print(f"\n[HISTÓRICO COMPLETO DE EVOLUÇÕES CLÍNICAS] (Total: {len(prontuario.evolucoes)})")
    if not prontuario.evolucoes:
        print("  Nenhuma evolução clínica registrada até o momento.")
    else:
        for idx, ev in enumerate(prontuario.evolucoes, start=1):
            print(f"  --- Evolução {idx} (ID Evolução: #{ev.id} | Atendimento FK: #{ev.atendimento_id}) ---")
            print(f"      Data/Hora         : {ev.data_hora}")
            print(f"      Médico Autor      : [ID #{ev.medico_id}] {ev.medico_autor}")
            print(f"      Dias de Intubação : {ev.dias_entubacao}")
            print(f"      Relato Clínico    : {ev.relato}")
            print(f"      Diagnósticos (CID): {len(ev.diagnosticos)} vinculado(s)")
            for cid in ev.diagnosticos:
                print(f"         -> Código CID: {cid.codigo} | Descrição: {cid.descricao}")

    print("=" * 75)


def configurar_banco(db: BancoDeTeste):
    db.execute("CREATE TABLE paciente (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf TEXT, data_nascimento TEXT)")
    db.execute("CREATE TABLE medico (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, crm TEXT)")
    db.execute("CREATE TABLE enfermeiro (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, coren TEXT)")
    db.execute("CREATE TABLE CID (codigo VARCHAR(10) PRIMARY KEY, descricao VARCHAR(255))")

    db.execute("""
        CREATE TABLE atendimento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora_entrada TIMESTAMP,
            data_hora_alta TIMESTAMP,
            status TEXT,
            cor_risco TEXT,
            paciente_id INTEGER,
            medico_id INTEGER
        )
    """)
    db.execute("""
        CREATE TABLE triagem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pressao_arterial TEXT,
            temperatura REAL,
            saturacao INTEGER,
            data_hora TIMESTAMP,
            atendimento_id INTEGER,
            enfermeiro_id INTEGER
        )
    """)
    db.execute("""
        CREATE TABLE evolucao_clinica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            relato_clinico_observacoes VARCHAR(1000),
            dias_entubacao INTEGER,
            data_hora TIMESTAMP,
            atendimento_id INTEGER,
            medico_id INTEGER
        )
    """)
    db.execute("""
        CREATE TABLE diagnostico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Evolucao_Clinicaid INTEGER,
            CIDcodigo VARCHAR(10)
        )
    """)

    # Cadastrando Pacientes, APENAS 1 MÉDICO, 1 Enfermeiro e Catálogo CID
    db.execute("INSERT INTO paciente (nome, cpf, data_nascimento) VALUES ('Carlos Mendes', '111.222.333-44', '1988-02-10')")
    db.execute("INSERT INTO paciente (nome, cpf, data_nascimento) VALUES ('Ana Costa', '123.456.789-00', '1995-04-12')")
    db.execute("INSERT INTO medico (nome, crm) VALUES ('Dr. Roberto Alves', 'CRM-RJ 554433')")
    db.execute("INSERT INTO enfermeiro (nome, coren) VALUES ('Enf. Marcos Silva', 'COREN-RJ 112233')")

    db.execute("INSERT INTO CID (codigo, descricao) VALUES ('A90', 'Dengue [dengue clássico]')")
    db.execute("INSERT INTO CID (codigo, descricao) VALUES ('R50.9', 'Febre não especificada')")
    db.commit()


def executar_fluxo_hospitalar():
    print("=" * 75)
    print("SIMULAÇÃO DO FLUXO HOSPITALAR PASSO A PASSO - SISTEMA BIOLIFE")
    print("=" * 75)

    db = BancoDeTeste()
    configurar_banco(db)

    atend_repo = AtendimentoRepository(db)
    triagem_repo = TriagemRepository(db)
    evolucao_repo = EvolucaoRepositori(db)
    fila_prioridade = FilaManchester()

    # ------------------------------------------------------------------
    # ETAPA 1: FLUXO DETALHADO DE RECEPÇÃO, TRIAGEM E FILA DE PRIORIDADE
    # ------------------------------------------------------------------
    print("\n[ETAPA 1] FLUXO DE RECEPÇÃO, TRIAGEM E FORMAÇÃO DA FILA DE PRIORIDADE:")

    # --- Paciente 1: Carlos chega primeiro (08:00) ---
    print("\n  1.1) [08:00] Recepção: Carlos Mendes dá entrada no hospital (Status: AGUARDANDO_TRIAGEM).")
    id_atend_carlos = atend_repo.criar_novo_atendimento(
        Atendimento(None, "AGUARDANDO_TRIAGEM", "AZUL", "2026-11-04 08:00:00", paciente_id=1)
    )

    print("  1.2) [08:05] Sala de Triagem: Enf. Marcos afere sinais do Carlos (PA: 120/80 | Temp: 36.5°C | Sat: 99%).")
    triagem_repo.inserir_triagem(Triagem(None, "120/80", 36.5, 99, "2026-11-04 08:05:00", id_atend_carlos, 1))

    ficha_carlos = atend_repo.buscar_simples_por_id(id_atend_carlos)
    ficha_carlos.status = "AGUARDANDO_MEDICO"
    ficha_carlos.cor_risco = "VERDE"  # Pouco urgente
    atend_repo.atualizar_dados_atendimento(ficha_carlos)
    print("  1.3) [08:05] Classificação definida para Carlos: VERDE (Pouco Urgente). Enviado para a fila!")
    fila_prioridade.adicionar_paciente(ficha_carlos, "Carlos Mendes", "08:05")
    fila_prioridade.exibir_painel_fila()

    # --- Paciente 2: Ana Costa chega depois (08:10), mas em estado grave ---
    print("\n  1.4) [08:10] Recepção: Ana Costa dá entrada passando mal (Status: AGUARDANDO_TRIAGEM).")
    id_atend_ana = atend_repo.criar_novo_atendimento(
        Atendimento(None, "AGUARDANDO_TRIAGEM", "AZUL", "2026-11-04 08:10:00", paciente_id=2)
    )

    print("  1.5) [08:12] Sala de Triagem: Enf. Marcos realiza 1ª aferição da Ana (PA: 90/60 | Temp: 39.0°C | Sat: 91%).")
    id_t1_ana = triagem_repo.inserir_triagem(Triagem(None, "90/60", 39.0, 91, "2026-11-04 08:12:00", id_atend_ana, 1))

    print("       -> [UPDATE Triagem]: Enf. Marcos revisa o termômetro e corrige a temperatura de 39.0°C para 39.5°C.")
    t1_salva = triagem_repo.buscar_simples_por_id(id_t1_ana)
    t1_salva.temperatura = 39.5
    triagem_repo.Atualizar_Triagem(t1_salva)

    print("       -> [DELETE Triagem]: Uma triagem duplicada/zerada lançada por esbarrão no sistema é excluída.")
    id_t_errada = triagem_repo.inserir_triagem(Triagem(None, "000/000", 0.0, 0, "2026-11-04 08:13:00", id_atend_ana, 1))
    triagem_repo.excluir_triagem_errada(id_t_errada)

    ficha_ana = atend_repo.buscar_simples_por_id(id_atend_ana)
    ficha_ana.status = "AGUARDANDO_MEDICO"
    ficha_ana.cor_risco = "VERMELHO"  # Emergência!
    atend_repo.atualizar_dados_atendimento(ficha_ana)
    print("  1.6) [08:14] Classificação definida para Ana Costa: VERMELHO (Emergência).")
    print("       -> Ana entra na Fila de Prioridade e assume a 1ª posição na frente do Carlos!")
    fila_prioridade.adicionar_paciente(ficha_ana, "Ana Costa", "08:14")
    fila_prioridade.exibir_painel_fila()

    # ------------------------------------------------------------------
    # ETAPA 2: MÉDICO CHAMA DA FILA E VISUALIZA O PRONTUÁRIO DA ANA
    # ------------------------------------------------------------------
    nome_chamado, ficha_chamada = fila_prioridade.chamar_proximo()
    print(f"\n[ETAPA 2] CHAMADA NO CONSULTÓRIO MÉDICO (Dr. Roberto Alves):")
    print(f"  -> O sistema chama o 1º da fila: {nome_chamado} (Atendimento #{ficha_chamada.id} | Risco: {ficha_chamada.cor_risco})")
    print("  -> Dr. Roberto abre o Prontuário Completo na tela para ler a triagem antes de evoluir:")

    prontuario_na_consulta = atend_repo.buscar_prontuario(ficha_chamada.id)
    imprimir_prontuario_completo(prontuario_na_consulta, "VISÃO DO DR. ROBERTO AO CHAMAR A PACIENTE - ANTES DA EVOLUÇÃO")

    # ------------------------------------------------------------------
    # ETAPA 3: DR. ROBERTO REGISTRA A EVOLUÇÃO CLÍNICA E OS CIDs
    # ------------------------------------------------------------------
    print(f"\n[ETAPA 3] REGISTRO DE EVOLUÇÃO CLÍNICA E DIAGNÓSTICOS (Dr. Roberto Alves):")

    evo = Evolucao(
        id_evolucao=None,
        relato="Paciente avaliada em emergência com febre alta (39.5°C), hipotensão e dor retro-orbital.",
        data_hora="2026-11-04 08:30:00",
        dias_entubacao=0,
        atendimento_id=ficha_chamada.id,
        medico_id=1  # Dr. Roberto Alves (Único médico)
    )
    id_evo = evolucao_repo.Inserir_Evolucao(evo)
    print(f"  -> [INSERT Evolução]: Evolução #{id_evo} criada pelo Dr. Roberto Alves.")

    evolucao_repo.vincular_diagnostico(id_evo, "A90")
    evolucao_repo.vincular_diagnostico(id_evo, "R50.9")
    print("  -> [INSERT Diagnósticos N:N]: CIDs 'A90' (Dengue) e 'R50.9' (Febre) vinculados à Evolução.")

    evo_salva = evolucao_repo.buscar_simples_por_id(id_evo)
    evo_salva.relato = "Paciente com febre alta (39.5°C) e dor retro-orbital. Hidratação venosa concluída; quadro estabilizado."
    evolucao_repo.Atualizar_Evolucao(evo_salva)
    print(f"  -> [UPDATE Evolução]: Dr. Roberto atualiza o relato da Evolução #{id_evo} após medicar a paciente.")

    id_evo_errada = evolucao_repo.Inserir_Evolucao(
        Evolucao(None, "Rascunho duplicado", "2026-11-04 08:35:00", 0, ficha_chamada.id, 1)
    )
    evolucao_repo.vincular_diagnostico(id_evo_errada, "A90")
    evolucao_repo.excluir_evolucao(id_evo_errada)
    print(f"  -> [DELETE Evolução]: Rascunho duplicado (#{id_evo_errada}) e seus vínculos excluídos com sucesso.")

    # ------------------------------------------------------------------
    # ETAPA 4: DR. ROBERTO DÁ ALTA E VISUALIZA O PRONTUÁRIO FINAL DA ANA
    # ------------------------------------------------------------------
    ficha_chamada.status = StatusAtendimento.ALTA.value if hasattr(StatusAtendimento, "ALTA") else "ALTA_MEDICA"
    ficha_chamada.medico_id = 1  # Dr. Roberto Alves assina a alta
    ficha_chamada.data_alta = "2026-11-04 16:00:00"
    atend_repo.atualizar_dados_atendimento(ficha_chamada)
    print(f"\n[ETAPA 4] ALTA MÉDICA E FECHAMENTO DO PRONTUÁRIO:")
    print(f"  -> Dr. Roberto Alves (ID #{ficha_chamada.medico_id}) assina a alta de {nome_chamado} às {ficha_chamada.data_alta}!")

    prontuario_final = atend_repo.buscar_prontuario(ficha_chamada.id)
    imprimir_prontuario_completo(prontuario_final, "PRONTUÁRIO FINAL DA PACIENTE APÓS EVOLUÇÃO E ALTA MÉDICA")


if __name__ == "__main__":
    executar_fluxo_hospitalar()