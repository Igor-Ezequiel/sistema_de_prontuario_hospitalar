from src.models.Classes import Paciente
from src.repositori.UsuarioRepositori import UsuarioRepositori

class PacienteRepositori:

    def __init__(self, db_conexao):
        self.db = db_conexao
        self.usuario_repo = UsuarioRepositori(db_conexao)

    def inserir_paciente(self, paciente: Paciente) -> int:
        sql = """
            INSERT INTO paciente (nome, cpf, data_nascimento, usuario_id)
            VALUES (:nome, :cpf, :data_nasc, :usuario_id)
            RETURNING id
        """
        resultado = self.db.execute(sql, {
            "nome": paciente.nome,
            "cpf": paciente.cpf,
            "data_nasc": paciente.data_nascimento,
            "usuario_id": paciente.usuario_id
        }).fetchone()

        self.db.commit()
        return resultado.id

    def buscar_por_id(self, id_paciente: int) -> Paciente:
        sql = """
            SELECT id, nome, cpf, data_nascimento, usuario_id
            FROM paciente
            WHERE id = :id
        """
        linha = self.db.execute(sql, {"id": id_paciente}).fetchone()

        if not linha:
            return None

        paciente = Paciente(
            id_paciente=linha.id,
            nome=linha.nome,
            cpf=linha.cpf,
            data_nascimento=linha.data_nascimento,
            usuario_id=linha.usuario_id
        )

        
        if paciente.usuario_id:
            paciente.usuario = self.usuario_repo.buscar_por_id(paciente.usuario_id)

        return paciente

    def buscar_por_cpf(self, cpf: str) -> Paciente:
        sql = """
            SELECT id, nome, cpf, data_nascimento, usuario_id
            FROM paciente
            WHERE cpf = :cpf
        """
        linha = self.db.execute(sql, {"cpf": cpf}).fetchone()

        if not linha:
            return None

        paciente = Paciente(
            id_paciente=linha.id,
            nome=linha.nome,
            cpf=linha.cpf,
            data_nascimento=linha.data_nascimento,
            usuario_id=linha.usuario_id
        )

        if paciente.usuario_id:
            paciente.usuario = self.usuario_repo.buscar_por_id(paciente.usuario_id)

        return paciente

    def atualizar_paciente(self, paciente: Paciente):
        sql = """
            UPDATE paciente
            SET nome = :nome,
                cpf = :cpf,
                data_nascimento = :data_nasc,
                usuario_id = :usuario_id
            WHERE id = :id
        """
        self.db.execute(sql, {
            "nome": paciente.nome,
            "cpf": paciente.cpf,
            "data_nasc": paciente.data_nascimento,
            "usuario_id": paciente.usuario_id,
            "id": paciente.id
        })
        self.db.commit()

    def excluir_paciente(self, id_paciente: int):
        sql = "DELETE FROM paciente WHERE id = :id"
        self.db.execute(sql, {"id": id_paciente})
        self.db.commit()