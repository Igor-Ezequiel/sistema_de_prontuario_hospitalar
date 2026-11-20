from src.models.Classes import Coordenador
from src.repositori.Equipe_Medica.UsuarioRepository import UsuarioRepository

class CoordenadorRepository:

    def __init__(self, db_conexao):
        self.db = db_conexao
        self.usuario_repo = UsuarioRepository(db_conexao)

    def inserir_coordenador(self, coordenador: Coordenador) -> int:
        id_gerado = self.usuario_repo.inserir_usuario(coordenador)
        coordenador.id = id_gerado

        sql = """
            INSERT INTO coordenador (id, nome, setor_responsavel)
            VALUES (:id, :nome, :setor)
        """
        self.db.execute(sql, {
            "id": coordenador.id,
            "nome": coordenador.nome,
            "setor": coordenador.setor_responsavel
        })
        self.db.commit()
        return coordenador.id

    def buscar_por_id(self, id_coordenador: int) -> Coordenador:
        sql = """
            SELECT c.id, c.nome, c.setor_responsavel,
                   u.email, u.senha, u.cpf, u.ativo
            FROM coordenador c
            INNER JOIN usuario u ON c.id = u.id
            WHERE c.id = :id
        """
        linha = self.db.execute(sql, {"id": id_coordenador}).fetchone()

        if not linha:
            return None

        return Coordenador(
            id_coordenador=linha.id,
            nome=linha.nome,
            setor_responsavel=linha.setor_responsavel,
            email=linha.email,
            senha=linha.senha,
            ativo=bool(linha.ativo),
            cpf=linha.cpf
        )

    def atualizar_coordenador(self, coordenador: Coordenador):
        self.usuario_repo.atualizar_usuario(coordenador)

        sql = """
            UPDATE coordenador
            SET nome = :nome,
                setor_responsavel = :setor
            WHERE id = :id
        """
        self.db.execute(sql, {
            "nome": coordenador.nome,
            "setor": coordenador.setor_responsavel,
            "id": coordenador.id
        })
        self.db.commit()

    def desativar_coordenador(self, id_coordenador: int):
        self.usuario_repo.desativar_usuario(id_coordenador)