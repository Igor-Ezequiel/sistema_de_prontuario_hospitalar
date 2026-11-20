from src.models.Classes import Plantao, Medico, Coordenador
from src.repositori.Equipe_Medica.MedicoRepository import MedicoRepository
from src.repositori.Equipe_Medica.CoordenadorRepository import CoordenadorRepository

class PlantaoRepository:

    def __init__(self, db_conexao):
        self.db = db_conexao
        
        self.medico_repo = MedicoRepository(db_conexao)
        self.coordenador_repo = CoordenadorRepository(db_conexao)

    def inserir_plantao(self, plantao: Plantao) -> int:
        sql = """
            INSERT INTO plantao (setor_ala, data_hora_inicio, data_hora_fim, medico_id, coordenador_id)
            VALUES (:setor, :inicio, :fim, :medico_id, :coordenador_id)
            RETURNING id
        """
        resultado = self.db.execute(sql, {
            "setor": plantao.setor_ala,
            "inicio": plantao.data_hora_inicio,
            "fim": plantao.data_hora_fim,
            "medico_id": plantao.medico_id,
            "coordenador_id": plantao.coordenador_id
        }).fetchone()

        self.db.commit()
        return resultado.id


    def atualizar_plantao(self, plantao: Plantao):
        sql = """
            UPDATE plantao
            SET setor_ala = :setor,
                data_hora_inicio = :inicio,
                data_hora_fim = :fim,
                medico_id = :medico_id,
                coordenador_id = :coordenador_id
            WHERE id = :id
        """
        self.db.execute(sql, {
            "setor": plantao.setor_ala,
            "inicio": plantao.data_hora_inicio,
            "fim": plantao.data_hora_fim,
            "medico_id": plantao.medico_id,
            "coordenador_id": plantao.coordenador_id,
            "id": plantao.id
        })
        self.db.commit()
        
       
    def buscar_por_id(self, id_plantao: int) -> Plantao:
        sql = """
            SELECT id, setor_ala, data_hora_inicio, data_hora_fim, medico_id, coordenador_id
            FROM plantao
            WHERE id = :id
        """
        linha = self.db.execute(sql, {"id": id_plantao}).fetchone()

        if not linha:
            return None

       
        return Plantao(
            id_plantao=linha.id,
            setor_ala=linha.setor_ala,
            data_hora_inicio=linha.data_hora_inicio,
            data_hora_fim=linha.data_hora_fim,
            medico_id=linha.medico_id,
            coordenador_id=linha.coordenador_id
        )


    def buscar_detalhes_por_id(self, id_plantao: int) -> Plantao:
        
        sql = """
            SELECT p.id, p.setor_ala, p.data_hora_inicio, p.data_hora_fim, 
                   p.medico_id, p.coordenador_id,
                   m.nome AS medico_nome, m.crm, m.especialidade_medica_id AS especialidade,
                   c.nome AS coordenador_nome, c.setor_responsavel
            FROM plantao p
            INNER JOIN medico m ON p.medico_id = m.id
            INNER JOIN coordenador c ON p.coordenador_id = c.id
            WHERE p.id = :id
        """
        linha = self.db.execute(sql, {"id": id_plantao}).fetchone()

        if not linha:
            return None

        plantao = Plantao(
            id_plantao=linha.id,
            setor_ala=linha.setor_ala,
            data_hora_inicio=linha.data_hora_inicio,
            data_hora_fim=linha.data_hora_fim,
            medico_id=linha.medico_id,
            coordenador_id=linha.coordenador_id
        )

        plantao.medico = Medico(
            id_medico=linha.medico_id, 
            nome=linha.medico_nome, 
            crm=linha.crm, 
            especialidade=linha.especialidade
        )
        plantao.coordenador = Coordenador(
            id_coordenador=linha.coordenador_id, 
            nome=linha.coordenador_nome, 
            setor_responsavel=linha.setor_responsavel
        )

        return plantao

    def verificar_plantao_ativo(self, medico_id: int, hora_atual) -> bool:
        
        sql = """
            SELECT 1 
            FROM plantao 
            WHERE medico_id = :medico_id 
            AND data_hora_inicio <= :hora_atual 
            AND data_hora_fim >= :hora_atual
        """
        resultado = self.db.execute(sql, {"medico_id": medico_id, "hora_atual": hora_atual}).fetchone()
        
        return resultado is not None
    
    
    def excluir_plantao(self, id_plantao: int):
        sql = "DELETE FROM plantao WHERE id = :id"
        self.db.execute(sql, {"id": id_plantao})
        self.db.commit()

    