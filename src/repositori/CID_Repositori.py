from src.models.Classes import CID

class CIDRepository:
    def __init__(self, db_conexao):
        self.db = db_conexao

    def buscar_simples_por_id(self, codigo: str) -> CID:
        sql = """
            SELECT codigo, descricao
            FROM CID
            WHERE codigo = :codigo
        """
        linha = self.db.execute(sql, {"codigo": codigo}).fetchone()

        if not linha:
            return None

        return CID(
            codigo=linha.codigo,
            descricao=linha.descricao 
        )