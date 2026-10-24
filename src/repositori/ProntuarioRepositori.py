from datetime import datetime
from models import (
    Atendimento, Paciente, Medico, 
    Triagem, Evolucao, StatusAtendimento, CorRisco
)

class AtendimentoRepository:
    def __init__(self, db_conexao):
        self.db = db_conexao

    def criar_novo_atendimento(self, paciente_id: int) -> int:
        sql = """
            INSERT INTO atendimento (data_hora_entrada, status, cor_risco, paciente_id) 
            VALUES (:data_agora, :status_inicial, :cor_inicial, :pac_id)
            RETURNING id
        """
        resultado = self.db.execute(sql, {
            "data_agora": datetime.now(),
            "status_inicial": StatusAtendimento.AGUARDANDO_TRIAGEM.value,
            "cor_inicial": CorRisco.CINZA.value,
            "pac_id": paciente_id
        }).fetchone()
        
        self.db.commit()
        return resultado.id  

    def buscar_simples_por_id(self, atendimento_id: int) -> Atendimento:
        sql = """
            SELECT id, data_hora_entrada, data_hora_alta, status, cor_risco 
            FROM atendimento 
            WHERE id = :id
        """
        linha = self.db.execute(sql, {"id": atendimento_id}).fetchone()
        
        if not linha:
            return None
            
        return Atendimento(
            atendimento_id = linha.id,
            status = linha.status,
            cor_risco = linha.cor_risco,
            data_entrada = linha.data_hora_entrada,
            data_alta = linha.data_hora_alta
        )

    def atualizar_dados_atendimento(self, atendimento_id: int, novo_status: StatusAtendimento, cor_risco: CorRisco, medico_id: int = None):
        sql = """
            UPDATE atendimento 
            SET 
                status = :status, 
                cor_risco = :cor,
                medico_id = :med_id
            WHERE id = :id
        """
        self.db.execute(sql, {
            "status": novo_status,
            "cor": cor_risco,
            "med_id": medico_id,
            "id": atendimento_id
        })
        self.db.commit()

    def cancelar_atendimento(self, atendimento_id: int):
        sql = """
            UPDATE atendimento 
            SET status = :status_cancelado 
            WHERE id = :id
        """
        self.db.execute(sql, {
            "status_cancelado": StatusAtendimento.CANCELADO.value,
            "id": atendimento_id
        })
        self.db.commit()

    def registrar_alta_paciente(self, atendimento_id: int):
        sql = """
            UPDATE atendimento 
            SET 
                status = :status_alta, 
                data_hora_alta = :data_agora
            WHERE id = :id
        """
        self.db.execute(sql, {
            "status_alta": StatusAtendimento.ALTA.value,
            "data_agora": datetime.now(),
            "id": atendimento_id
        })
        self.db.commit()
        
    def buscar_prontuario_completo(self, atendimento_id: int) -> Atendimento:
        sql_capa = """
            SELECT 
                a.id, a.status, a.cor_risco, a.data_hora_entrada, a.data_hora_alta,
                p.id AS pac_id, p.nome AS pac_nome, p.cpf, p.data_nascimento,
                m.id AS med_id, m.nome AS med_nome, m.crm
            FROM atendimento a
            INNER JOIN paciente p ON a.paciente_id = p.id
            LEFT JOIN medico m ON a.medico_id = m.id
            WHERE a.id = :id
        """
        base = self.db.execute(sql_capa, {"id": atendimento_id}).fetchone()

        if not base:
            return None

        # Instancia a classe Atendimento
        prontuario = Atendimento(
            atendimento_id = base.id,
            status = base.status,
            cor_risco = base.cor_risco,
            data_entrada = base.data_hora_entrada,
            data_alta = base.data_hora_alta
        )

        prontuario.paciente = Paciente(
            id_paciente = base.pac_id,
            nome = base.pac_nome,
            cpf = base.cpf,
            data_nascimento = base.data_nascimento
        )

        if base.med_id is not None:
            prontuario.medico = Medico(
                id_medico = base.med_id,
                nome = base.med_nome,
                crm = base.crm
            )

        sql_triagens = """
            SELECT id, pressao_arterial, temperatura, saturacao, data_hora
            FROM triagem
            WHERE atendimento_id = :id
            ORDER BY data_hora DESC
        """
        linhas_triagem = self.db.execute(sql_triagens, {"id": atendimento_id}).fetchall()

        for t in linhas_triagem:
            objeto_triagem = Triagem(
                id_triagem = t.id,
                pressao = t.pressao_arterial,
                temperatura = t.temperatura,
                saturacao = t.saturacao,
                data_hora = t.data_hora
            )
            prontuario.triagens.append(objeto_triagem)

        sql_evolucoes = """
            SELECT e.id, e.relato_clinico_observacoes, e.dias_entubacao, e.data_hora,
                   m.nome AS medico_autor
            FROM evolucao_clinica e
            INNER JOIN medico m ON e.medico_id = m.id
            WHERE e.atendimento_id = :id
            ORDER BY e.data_hora DESC
        """
        linhas_evolucao = self.db.execute(sql_evolucoes, {"id": atendimento_id}).fetchall()

        for e in linhas_evolucao:
            objeto_evolucao = Evolucao(
                id_evolucao = e.id,
                relato = e.relato_clinico_observacoes,
                dias_entubacao = e.dias_entubacao,
                data_hora = e.data_hora,
                medico_autor = e.medico_autor
            )
            prontuario.evolucoes.append(objeto_evolucao)

        return prontuario