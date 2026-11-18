from datetime import datetime

class PermissaoExtraRepositori:
    
    def inserir_permissao(self, atendimento_id: int, medico_id: int, coordenador_id: int, motivo: str) -> int: 
        
        sql = """
            INSERT INTO Permissao_Extra (data_hora_liberacao, motivo, validade, Medicoid, Atendimentoid, Coordenadorid) 
            VALUES (:data_hora_liberacao, :motivo, :validade, :medico_id, :atendimento_id, :coordenador_id)
            RETURNING id
        """
        
        resultado = self.db.execute(sql, {
            "data_hora_liberacao": datetime.now(),
            "motivo": motivo,
            "validade": None,
            "medico_id": medico_id,
            "atendimento_id": atendimento_id,
            "coordenador_id": coordenador_id
        }).fetchone()
        
        return resultado[0]
    
    