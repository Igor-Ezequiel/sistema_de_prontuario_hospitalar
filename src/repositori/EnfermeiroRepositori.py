from src.models.Classes import Enfermeiro
from src.repositori.UsuarioRepositori import UsuarioRepositori

class EnfermeiroRepositori:

    def __init__(self, db_conexao):
        self.db = db_conexao
        self.usuario_repo = UsuarioRepositori(db_conexao)

    def inserir_enfermeiro(self, enfermeiro: Enfermeiro) -> int:
        id_gerado = self.usuario_repo.inserir_usuario(enfermeiro)
        enfermeiro.id = id_gerado

        sql = """
            INSERT INTO enfermeiro (id, nome, coren)
            VALUES (:id, :nome, :coren)
        """
        self.db.execute(sql, {
            "id": enfermeiro.id,
            "nome": enfermeiro.nome,
            "coren": enfermeiro.coren
        })
        self.db.commit()
        return enfermeiro.id

    def buscar_por_id(self, id_enfermeiro: int) -> Enfermeiro:
        sql = """
            SELECT e.id, e.nome, e.coren,
                   u.email, u.senha, u.ativo
            FROM enfermeiro e
            INNER JOIN usuario u ON e.id = u.id
            WHERE e.id = :id
        """
        linha = self.db.execute(sql, {"id": id_enfermeiro}).fetchone()

        if not linha:
            return None

        return Enfermeiro(
            id_enfermeiro=linha.id,
            nome=linha.nome,
            coren=linha.coren,
            email=linha.email,
            senha=linha.senha,
            ativo=bool(linha.ativo)
        )

    def buscar_por_coren(self, coren: str) -> Enfermeiro:
        sql = """
            SELECT e.id, e.nome, e.coren,
                   u.email, u.senha, u.ativo
            FROM enfermeiro e
            INNER JOIN usuario u ON e.id = u.id
            WHERE e.coren = :coren
        """
        linha = self.db.execute(sql, {"coren": coren}).fetchone()

        if not linha:
            return None

        return Enfermeiro(
            id_enfermeiro=linha.id,
            nome=linha.nome,
            coren=linha.coren,
            email=linha.email,
            senha=linha.senha,
            ativo=bool(linha.ativo)
        )

    def atualizar_enfermeiro(self, enfermeiro: Enfermeiro):
        self.usuario_repo.atualizar_usuario(enfermeiro)

        sql = """
            UPDATE enfermeiro
            SET nome = :nome,
                coren = :coren
            WHERE id = :id
        """
        self.db.execute(sql, {
            "nome": enfermeiro.nome,
            "coren": enfermeiro.coren,
            "id": enfermeiro.id
        })
        self.db.commit()

    def desativar_enfermeiro(self, id_enfermeiro: int):
        self.usuario_repo.desativar_usuario(id_enfermeiro)