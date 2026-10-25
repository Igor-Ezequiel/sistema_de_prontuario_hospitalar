from src.models.Classes import Triagem

class TriagemRepository:
    def __init__(self, db_conexao):
        self.db = db_conexao

    # 1. CREATE: Insere uma nova avaliação mantendo o histórico
    def inserir_triagem(self, ficha_triagem: Triagem, atendimento_id: int, enfermeiro_id: int) -> int:
        sql = """
            INSERT INTO triagem (pressao_arterial, temperatura, saturacao, data_hora, Atendimentoid, Enfermerioid)
            VALUES (:pressao, :temp, :sat, :data_hora, :atend_id, :enf_id)
            RETURNING id
        """
        resultado = self.db.execute(sql, {
            "pressao": ficha_triagem.pressao,
            "temp": ficha_triagem.temperatura,
            "sat": ficha_triagem.saturacao,
            "data_hora": ficha_triagem.data_hora,
            "atend_id": atendimento_id,
            "enf_id": enfermeiro_id
        }).fetchone()
        
        self.db.commit()
        return resultado.id

    # 2. READ: Devolve a lista completa de triagens do paciente (a mais recente na posição [0])
    def buscar_historico_por_atendimento(self, atendimento_id: int) -> list[Triagem]:
        sql = """
            SELECT id, pressao_arterial, temperatura, saturacao, data_hora
            FROM triagem
            WHERE Atendimentoid = :id
            ORDER BY data_hora DESC
        """
        linhas = self.db.execute(sql, {"id": atendimento_id}).fetchall()

        historico = []
        for linha in linhas:
            triagem_obj = Triagem(
                id_triagem=linha.id,
                pressao=linha.pressao_arterial,
                temperatura=linha.temperatura,
                saturacao=linha.saturacao,
                data_hora=linha.data_hora
            )
            historico.append(triagem_obj)

        return historico

    # 3. UPDATE: Restrito à correção de erros de digitação (ex: 380ºC em vez de 38.0ºC)
    def corrigir_erro_digitacao(self, triagem_id: int, nova_pressao: str, nova_temp: float, nova_sat: float):
        sql = """
            UPDATE triagem
            SET pressao_arterial = :pressao,
                temperatura = :temp,
                saturacao = :sat
            WHERE id = :id
        """
        self.db.execute(sql, {
            "pressao": nova_pressao,
            "temp": nova_temp,
            "sat": nova_sat,
            "id": triagem_id
        })
        self.db.commit()

    # 4. DELETE: Exclusão física (apenas para casos onde a triagem foi registada na ficha do paciente errado)
    def excluir_triagem_errada(self, triagem_id: int):
        sql = "DELETE FROM triagem WHERE id = :id"
        self.db.execute(sql, {"id": triagem_id})
        self.db.commit()