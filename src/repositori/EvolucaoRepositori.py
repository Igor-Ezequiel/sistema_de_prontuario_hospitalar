from src.models.Classes import Evolucao, CID

class EvolucaoRepositori:
    
    def __init__(self, db_conexao):
        self.db = db_conexao
        
    def Inserir_Evolucao(self, ficha_evolucao: Evolucao) -> int:
        sql = """
            INSERT INTO evolucao_clinica (relato_clinico_observacoes, dias_entubacao, data_hora, atendimento_id, medico_id)
            VALUES (:relato, :dias_entub, :data_hora, :atendi_id, :medico_id)
            RETURNING id
        """
        
        resultado = self.db.execute(sql, {
            "relato": ficha_evolucao.relato,
            "dias_entub": ficha_evolucao.dias_entubacao,
            "data_hora": ficha_evolucao.data_hora,
            "atendi_id": ficha_evolucao.atendimento_id,
            "medico_id": ficha_evolucao.medico_id
        }).fetchone()
        
        self.db.commit()
        return resultado.id
        
    def buscar_simples_por_id(self, id_evolucao: int) -> Evolucao:
        sql = """
            SELECT id, relato_clinico_observacoes AS relato, dias_entubacao, data_hora, atendimento_id, medico_id
            FROM evolucao_clinica
            WHERE id = :id 
        """
        
        linha = self.db.execute(sql, {"id": id_evolucao}).fetchone()
        
        if not linha:
             return None
         
        return Evolucao(
            id_evolucao=linha.id,
            relato=linha.relato,
            dias_entubacao=linha.dias_entubacao,
            data_hora=linha.data_hora,
            medico_id=linha.medico_id,
            atendimento_id=linha.atendimento_id
        )
        
    def buscar_diagnosticos_por_evolucao(self, evolucao_id: int) -> list[CID]:
        sql = """
            SELECT 
                c.codigo, 
                c.descricao
            FROM diagnostico d
            INNER JOIN CID c ON d.CIDcodigo = c.codigo
            WHERE d.Evolucao_Clinicaid = :id
        """
        
        linhas = self.db.execute(sql, {"id": evolucao_id}).fetchall()
        
        lista_cids = []
        for linha in linhas:
            cid_obj = CID(
                codigo=linha.codigo,
                descricao=linha.descricao
            )
            lista_cids.append(cid_obj)
            
        return lista_cids


    def Atualizar_Evolucao(self, evolucao_atualizada: Evolucao):
        sql = """
            UPDATE evolucao_clinica
            SET relato_clinico_observacoes = :relato,
                dias_entubacao = :dias_entub
            WHERE id = :id
        """
        
        self.db.execute(sql, {
            "relato": evolucao_atualizada.relato,
            "dias_entub": evolucao_atualizada.dias_entubacao,
            "id": evolucao_atualizada.id
        })
        
        self.db.commit()
        
    def excluir_evolucao(self, id_evolucao: int):
        
        sql_diagnosticos = "DELETE FROM diagnostico WHERE Evolucao_Clinicaid = :id"
        self.db.execute(sql_diagnosticos, {"id": id_evolucao})
        
        sql_evolucao = "DELETE FROM evolucao_clinica WHERE id = :id"
        self.db.execute(sql_evolucao, {"id": id_evolucao})
        
        self.db.commit()