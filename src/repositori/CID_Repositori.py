from src.models.Classes import (
    CID  
)

class CIDRepository:
    def __init__(self, db_conexao):
        self.db = db_conexao

    

    def buscar_simples_por_id(self, codigo: str) -> CID:
        sql = """
            SELECT codigo, descricao
            FROM CID
            WHERE id = :id
        """
        linha = self.db.execute(sql, {"id": atendimento_id}).fetchone()

        if not linha:
            return None

        return CID(
            codigo=linha.codigo,
            descricao=linha.descricao
            
        )

    