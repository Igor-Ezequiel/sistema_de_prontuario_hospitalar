from src.models.Classes import Medico
from src.repositori.UsuarioRepositori import UsuarioRepositori

class MedicoRepositori:

    def __init__(self, db_conexao):
        self.db = db_conexao
        self.usuario_repo = UsuarioRepositori(db_conexao)

    def inserir_medico(self, medico: Medico) -> int:
        # 1. Insere na tabela mãe (usuario) e recupera o ID gerado
        id_gerado = self.usuario_repo.inserir_usuario(medico)
        medico.id = id_gerado

        # 2. Insere na tabela filha (medico) usando o mesmo ID da herança
        sql = """
            INSERT INTO medico (id, nome, crm, especialidade)
            VALUES (:id, :nome, :crm, :especialidade)
        """
        self.db.execute(sql, {
            "id": medico.id,
            "nome": medico.nome,
            "crm": medico.crm,
            "especialidade": medico.especialidade
        })
        self.db.commit()
        return medico.id

    def buscar_por_id(self, id_medico: int) -> Medico:
        sql = """
            SELECT m.id, m.nome, m.crm, m.especialidade,
                   u.email, u.senha, u.ativo
            FROM medico m
            INNER JOIN usuario u ON m.id = u.id
            WHERE m.id = :id
        """
        linha = self.db.execute(sql, {"id": id_medico}).fetchone()

        if not linha:
            return None

        return Medico(
            id_medico=linha.id,
            nome=linha.nome,
            crm=linha.crm,
            especialidade=linha.especialidade,
            email=linha.email,
            senha=linha.senha,
            ativo=bool(linha.ativo)
        )

    def buscar_por_crm(self, crm: str) -> Medico:
        sql = """
            SELECT m.id, m.nome, m.crm, m.especialidade,
                   u.email, u.senha, u.ativo
            FROM medico m
            INNER JOIN usuario u ON m.id = u.id
            WHERE m.crm = :crm
        """
        linha = self.db.execute(sql, {"crm": crm}).fetchone()

        if not linha:
            return None

        return Medico(
            id_medico=linha.id,
            nome=linha.nome,
            crm=linha.crm,
            especialidade=linha.especialidade,
            email=linha.email,
            senha=linha.senha,
            ativo=bool(linha.ativo)
        )

    def atualizar_medico(self, medico: Medico):
        # Atualiza os dados de acesso na tabela mãe (usuario)
        self.usuario_repo.atualizar_usuario(medico)

        # Atualiza os dados profissionais na tabela filha (medico)
        sql = """
            UPDATE medico
            SET nome = :nome,
                crm = :crm,
                especialidade = :especialidade
            WHERE id = :id
        """
        self.db.execute(sql, {
            "nome": medico.nome,
            "crm": medico.crm,
            "especialidade": medico.especialidade,
            "id": medico.id
        })
        self.db.commit()

    def desativar_medico(self, id_medico: int):
        # Soft Delete herdado de Usuario para não quebrar prontuários antigos
        self.usuario_repo.desativar_usuario(id_medico)