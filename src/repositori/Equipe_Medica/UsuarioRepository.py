from src.models.Classes import Usuario

class UsuarioRepository:

    def __init__(self, db_conexao):
        self.db = db_conexao

    def inserir_usuario(self, novo_usuario: Usuario) -> int:
        sql = """
            INSERT INTO usuario (email, senha, cargo, cpf, ativo)
            VALUES (:email, :senha, :cargo, :cpf, :ativo)
            RETURNING id
        """
        resultado = self.db.execute(sql, {
            "email": novo_usuario.email,
            "senha": novo_usuario.senha,
            "cargo": novo_usuario.cargo,
            "cpf": novo_usuario.cpf,
            "ativo": novo_usuario.ativo
        }).fetchone()

        self.db.commit()
        return resultado.id

    def buscar_por_id(self, id_usuario: int) -> Usuario:
        sql = """
            SELECT id, email, senha, cargo, cpf, ativo
            FROM usuario
            WHERE id = :id
        """
        linha = self.db.execute(sql, {"id": id_usuario}).fetchone()

        if not linha:
            return None

        return Usuario(
            id_usuario=linha.id,
            email=linha.email,
            senha=linha.senha,
            cargo=linha.cargo,
            ativo=bool(linha.ativo),
            cpf=linha.cpf
        )

    def buscar_por_email(self, email: str) -> Usuario:
        sql = """
            SELECT id, email, senha, cargo, cpf, ativo
            FROM usuario
            WHERE email = :email
        """
        linha = self.db.execute(sql, {"email": email}).fetchone()

        if not linha:
            return None

        return Usuario(
            id_usuario=linha.id,
            email=linha.email,
            senha=linha.senha,
            cargo=linha.cargo,
            ativo=bool(linha.ativo),
            cpf=linha.cpf
        )

    def buscar_por_cpf(self, cpf: str) -> Usuario:
        cpf_limpo = "".join(filter(str.isdigit, cpf))
        sql = """
            SELECT id, email, senha, cargo, cpf, ativo
            FROM usuario
            WHERE cpf = :cpf
        """
        linha = self.db.execute(sql, {"cpf": cpf_limpo}).fetchone()

        if not linha:
            return None

        return Usuario(
            id_usuario=linha.id,
            email=linha.email,
            senha=linha.senha,
            cargo=linha.cargo,
            ativo=bool(linha.ativo),
            cpf=linha.cpf
        )

    def atualizar_usuario(self, usuario: Usuario):
        sql = """
            UPDATE usuario
            SET email = :email,
                senha = :senha,
                cargo = :cargo,
                cpf = :cpf,
                ativo = :ativo
            WHERE id = :id
        """
        self.db.execute(sql, {
            "email": usuario.email,
            "senha": usuario.senha,
            "cargo": usuario.cargo,
            "cpf": usuario.cpf,
            "ativo": usuario.ativo,
            "id": usuario.id
        })
        self.db.commit()

    def desativar_usuario(self, id_usuario: int):

        sql = "UPDATE usuario SET ativo = :ativo WHERE id = :id"
        self.db.execute(sql, {"ativo": False, "id": id_usuario})
        self.db.commit()