from src.models.Classes import Enfermeiro, Triagem

class TriagemRepositori:
    def __init__(self, db_conexao):
        self.db = db_conexao

    def inserir_triagem(self, ficha_triagem: Triagem) -> int:
        sql = """
            INSERT INTO triagem (pressao_arterial, temperatura, saturacao, data_hora, atendimento_id, enfermeiro_id)
            VALUES (:pressao, :temp, :sat, :data_hora, :atend_id, :enf_id)
            RETURNING id
        """
        resultado = self.db.execute(sql, {
            "pressao": ficha_triagem.pressao,
            "temp": ficha_triagem.temperatura,
            "sat": ficha_triagem.saturacao,
            "data_hora": ficha_triagem.data_hora,
            "atend_id": ficha_triagem.atendimento_id,
            "enf_id": ficha_triagem.enfermeiro_id
        }).fetchone()
        
        self.db.commit()
        return resultado.id

    def buscar_simples_por_id(self, triagem_id: int) -> Triagem:
        sql = """
            SELECT id, pressao_arterial, temperatura, saturacao, data_hora, atendimento_id, enfermeiro_id
            FROM triagem
            WHERE id = :id
        """
        linha = self.db.execute(sql, {"id": triagem_id}).fetchone()

       
        if not linha:
            return None

        
        return Triagem(
            id_triagem=linha.id,
            pressao=linha.pressao_arterial,
            temperatura=linha.temperatura,
            saturacao=linha.saturacao,
            data_hora=linha.data_hora,
            atendimento_id=linha.atendimento_id,
            enfermeiro_id=linha.enfermeiro_id
        )
        
    def buscar_historico_por_atendimento(self, atendimento_id: int) -> list[Triagem]:
        sql = """
            SELECT 
                t.id AS triagem_id, 
                t.pressao_arterial, 
                t.temperatura, 
                t.saturacao, 
                t.data_hora, 
                t.atendimento_id, 
                t.enfermeiro_id,
                e.id AS enf_id,     
                e.nome AS enf_nome, 
                e.coren
            FROM triagem t
            INNER JOIN enfermeiro e ON t.enfermeiro_id = e.id
            WHERE t.atendimento_id = :id
            ORDER BY t.data_hora DESC
        """
        linhas = self.db.execute(sql, {"id": atendimento_id}).fetchall()

        historico = []
        for linha in linhas:
            
            triagem_obj = Triagem(
                id_triagem=linha.triagem_id,
                pressao=linha.pressao_arterial,
                temperatura=linha.temperatura,
                saturacao=linha.saturacao,
                data_hora=linha.data_hora,
                atendimento_id=linha.atendimento_id,
                enfermeiro_id=linha.enfermeiro_id
            )
            
            triagem_obj.enfermeiro = Enfermeiro(
                id_enfermeiro=linha.enf_id,
                nome=linha.enf_nome,
                coren=linha.coren
            )
            historico.append(triagem_obj)

        return historico


    def Atualizar_Triagem(self, triagem_atualizada: Triagem):
        sql = """
            UPDATE triagem
            SET pressao_arterial = :pressao,
                temperatura = :temp,
                saturacao = :sat
            WHERE id = :id
        """
        self.db.execute(sql, {
            "pressao": triagem_atualizada.pressao,
            "temp": triagem_atualizada.temperatura,
            "sat": triagem_atualizada.saturacao,
            "id": triagem_atualizada.id  
        })
        self.db.commit()

    def excluir_triagem_errada(self, triagem_id: int):
        
        sql = "DELETE FROM triagem WHERE id = :id"
        self.db.execute(sql, {"id": triagem_id})
        self.db.commit()