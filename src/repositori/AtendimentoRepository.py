from src.models.Classes import (
    Atendimento,
    Paciente,
    Medico,
    StatusAtendimento  
)

from repositori.TriagemRepository import TriagemRepository
from repositori.EvolucaoRepository import EvolucaoRepositori
from repositori.PermissaoExtraRepository import PermissaoExtraRepositori


class AtendimentoRepository:
    def __init__(self, db_conexao):
        self.db = db_conexao
        
        self.triagem_repo = TriagemRepository(db_conexao)
        self.evolucao_repo = EvolucaoRepositori(db_conexao)
        self.permissao_repo = PermissaoExtraRepositori(db_conexao)

    def inserir_atendimento(self, ficha: Atendimento) -> int:
        sql = """
            INSERT INTO atendimento (data_hora_entrada, status, cor_risco, paciente_id) 
            VALUES (:data_agora, :status_inicial, :cor_inicial, :pac_id)
            RETURNING id
        """
        resultado = self.db.execute(sql, {
            "data_agora": ficha.data_entrada,
            "status_inicial": ficha.status,
            "cor_inicial": ficha.cor_risco,
            "pac_id": ficha.paciente_id
        }).fetchone()

        self.db.commit()
        return resultado.id

    def buscar_simples_por_id(self, atendimento_id: int) -> Atendimento:
        sql = """
            SELECT id, data_hora_entrada, data_hora_alta, status, cor_risco, paciente_id, medico_id 
            FROM atendimento 
            WHERE id = :id
        """
        linha = self.db.execute(sql, {"id": atendimento_id}).fetchone()

        if not linha:
            return None

        return Atendimento(
            atendimento_id=linha.id,
            status=linha.status,
            cor_risco=linha.cor_risco,
            data_entrada=linha.data_hora_entrada,
            paciente_id=linha.paciente_id,
            data_alta=linha.data_hora_alta,
            medico_id=linha.medico_id
        )

    def atualizar_dados_atendimento(self, ficha: Atendimento):
        sql = """
            UPDATE atendimento 
            SET 
                status = :status, 
                cor_risco = :cor,
                medico_id = :med_id,
                data_hora_alta = :data_alta
            WHERE id = :id
        """
        self.db.execute(sql, {
            "status": ficha.status,
            "cor": ficha.cor_risco,
            "med_id": ficha.medico_id,
            "data_alta": ficha.data_alta,
            "id": ficha.id
        })
        self.db.commit()

    def deletar_atendimento(self, atendimento_id: int):
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

    def buscar_prontuario(self, atendimento_id: int) -> Atendimento:
        sql = """
            SELECT 
                a.id, a.status, a.cor_risco, a.data_hora_entrada, a.data_hora_alta,
                p.id AS pac_id, p.nome AS pac_nome, p.cpf, p.data_nascimento,
                m.id AS med_id, m.nome AS med_nome, m.crm
            FROM atendimento a
            INNER JOIN paciente p ON a.paciente_id = p.id
            LEFT JOIN medico m ON a.medico_id = m.id
            WHERE a.id = :id
        """
        base = self.db.execute(sql, {"id": atendimento_id}).fetchone()

        if not base:
            return None

        prontuario = Atendimento(
            atendimento_id=base.id,
            status=base.status,
            cor_risco=base.cor_risco,
            data_entrada=base.data_hora_entrada,
            paciente_id=base.pac_id,
            data_alta=base.data_hora_alta,
            medico_id=base.med_id
        )

        prontuario.paciente = Paciente(
            id_paciente=base.pac_id,
            nome=base.pac_nome,
            cpf=base.cpf,
            data_nascimento=base.data_nascimento
        )

        if base.med_id is not None:
            prontuario.medico = Medico(
                id_medico=base.med_id,
                nome=base.med_nome,
                crm=base.crm
            )

        prontuario.triagens = self.triagem_repo.buscar_historico_por_atendimento(atendimento_id)
        prontuario.evolucoes = self.evolucao_repo.buscar_historico_por_atendimento(atendimento_id)
        
        return prontuario
    
    def buscar_prontuario_para_auditoria(self, atendimento_id: int) -> Atendimento:
        
        prontuario = self.buscar_prontuario(atendimento_id)
        
        if not prontuario:
            return None
            
        prontuario.permissoes_extras = self.permissao_repo.buscar_permissoes_por_atendimento(atendimento_id)
        
        return prontuario
    
    