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
        
    def buscar_historico_por_atendimento(self, atendimento_id: int) -> list[Evolucao]:
        
        sql = """
            SELECT e.id, e.relato_clinico_observacoes, e.dias_entubacao, e.data_hora,
                   e.atendimento_id, e.medico_id, m.nome AS medico_autor
            FROM evolucao_clinica e
            INNER JOIN medico m ON e.medico_id = m.id
            WHERE e.atendimento_id = :id
            ORDER BY e.data_hora DESC
        """
        linhas = self.db.execute(sql, {"id": atendimento_id}).fetchall()

        historico = []
        for e in linhas:
            evolucao = Evolucao(
                id_evolucao=e.id,
                relato=e.relato_clinico_observacoes,
                data_hora=e.data_hora,
                dias_entubacao=e.dias_entubacao,
                atendimento_id=e.atendimento_id,
                medico_id=e.medico_id,
                medico_autor=e.medico_autor
            )
            
            
            evolucao.diagnosticos = self.buscar_diagnosticos_por_evolucao(evolucao.id)
            
            historico.append(evolucao)

        return historico

    def vincular_diagnostico(self, id_evolucao: int, codigo_cid: str):
    
        sql = """
            INSERT INTO diagnostico (Evolucao_Clinicaid, CIDcodigo)
            VALUES (:id_evo, :cod_cid)
        """
        self.db.execute(sql, {
            "id_evo": id_evolucao,
            "cod_cid": codigo_cid
        })
        self.db.commit()