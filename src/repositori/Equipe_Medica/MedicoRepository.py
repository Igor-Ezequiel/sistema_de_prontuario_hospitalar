from src.models.Classes import Medico
from src.repositori.Equipe_Medica.UsuarioRepository import UsuarioRepository


class MedicoRepository:

    def __init__(self, db_conexao):
        self.db = db_conexao
        self.usuario_repo = UsuarioRepository(db_conexao)

    def inserir_medico(self, medico: Medico) -> int:
        id_gerado = self.usuario_repo.inserir_usuario(medico)
        medico.id = id_gerado

        sql = """
            INSERT INTO medico (id, nome, crm, especialidade_medica_id)
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
            SELECT m.id, m.nome, m.crm, m.especialidade_medica_id AS especialidade,
                   u.email, u.senha, u.cpf, u.ativo
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
            ativo=bool(linha.ativo),
            cpf=linha.cpf
        )

    def buscar_por_crm(self, crm: str) -> Medico:
        sql = """
            SELECT m.id, m.nome, m.crm, m.especialidade_medica_id AS especialidade,
                   u.email, u.senha, u.cpf, u.ativo
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
            ativo=bool(linha.ativo),
            cpf=linha.cpf
        )

    def atualizar_medico(self, medico: Medico):
        self.usuario_repo.atualizar_usuario(medico)

        sql = """
            UPDATE medico
            SET nome = :nome,
                crm = :crm,
                especialidade_medica_id = :especialidade
            WHERE id = :id
        """
        self.db.execute(sql, {
            "nome": medico.nome,
            "crm": medico.crm,
            "especialidade": medico.especialidade,
            "id": medico.id
        })
        self.db.commit()

    def buscar_medicos_disponiveis(self, inicio_desejado, fim_desejado) -> list[Medico]:
        sql = """
            SELECT m.id, m.nome, m.crm, m.especialidade_medica_id AS especialidade,
                   u.email, u.cpf, u.ativo
            FROM medico m
            INNER JOIN usuario u ON m.id = u.id
            WHERE u.ativo = TRUE
              AND m.id NOT IN (
                  SELECT medico_id
                  FROM plantao
                  WHERE data_hora_inicio < :fim_desejado 
                    AND data_hora_fim > :inicio_desejado
              )
        """
        linhas = self.db.execute(sql, {
            "inicio_desejado": inicio_desejado, 
            "fim_desejado": fim_desejado
        }).fetchall()
        
        if not linhas:
            return []
        
        medicos_livres = []
        for linha in linhas:
            medico = Medico(
                id_medico=linha.id,
                nome=linha.nome,
                crm=linha.crm,
                especialidade=linha.especialidade,
                email=linha.email,
                ativo=bool(linha.ativo),
                cpf=linha.cpf
            )
            medicos_livres.append(medico)
            
        return medicos_livres

    def desativar_medico(self, id_medico: int):
        self.usuario_repo.desativar_usuario(id_medico)