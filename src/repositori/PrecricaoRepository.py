from src.models.Classes import Prescricao, Enfermeiro

class PrescricaoRepositori:

    def __init__(self, db_conexao):
        self.db = db_conexao

    def inserir_prescricao(self, prescricao: Prescricao) -> int:
       
        sql = """
            INSERT INTO prescricao (
                nome_medicamento, dose, intervalo_horas, status, 
                evolucao_id, enfermeiro_id, data_hora_aplicacao
            ) VALUES (
                :nome_medicamento, :dose, :intervalo_horas, :status, 
                :evolucao_id, :enfermeiro_id, :data_hora_aplicacao
            ) RETURNING id
        """
        
        resultado = self.db.execute(sql, {
            "nome_medicamento": prescricao.nome_medicamento,
            "dose": prescricao.dose,
            "intervalo_horas": prescricao.intervalo_horas,
            "status": prescricao.status,
            "evolucao_id": prescricao.evolucao_id,
            "enfermeiro_id": prescricao.enfermeiro_id,
            "data_hora_aplicacao": prescricao.data_hora_aplicacao
        }).fetchone()
        
        self.db.commit()
    
        return resultado.id

    def buscar_por_id(self, id_prescricao: int) -> Prescricao:
       
        sql = "SELECT * FROM prescricao WHERE id = :id"
        
        linha = self.db.execute(sql, {"id": id_prescricao}).fetchone()

        if not linha:
            return None

        return Prescricao(
            id_prescricao=linha.id,
            nome_medicamento=linha.nome_medicamento,
            dose=linha.dose,
            intervalo_horas=linha.intervalo_horas,
            status=linha.status,
            evolucao_id=linha.evolucao_id,
            enfermeiro_id=linha.enfermeiro_id,
            data_hora_aplicacao=linha.data_hora_aplicacao
        )

    def atualizar_prescricao(self, prescricao: Prescricao):
       
        sql = """
            UPDATE prescricao
            SET nome_medicamento = :nome_medicamento,
                dose = :dose,
                intervalo_horas = :intervalo_horas,
                status = :status,
                evolucao_id = :evolucao_id,
                enfermeiro_id = :enfermeiro_id,
                data_hora_aplicacao = :data_hora_aplicacao
            WHERE id = :id
        """
        self.db.execute(sql, {
            "nome_medicamento": prescricao.nome_medicamento,
            "dose": prescricao.dose,
            "intervalo_horas": prescricao.intervalo_horas,
            "status": prescricao.status,
            "evolucao_id": prescricao.evolucao_id,
            "enfermeiro_id": prescricao.enfermeiro_id,
            "data_hora_aplicacao": prescricao.data_hora_aplicacao,
            "id": prescricao.id
        })
        self.db.commit()

    def buscar_precricao_enfermeiro(self, id_prescricao: int) -> Prescricao:
        
        sql = """
            SELECT p.id, p.nome_medicamento, p.dose, p.intervalo_horas, 
                   p.status, p.evolucao_id, p.enfermeiro_id, p.data_hora_aplicacao,
                   e.nome AS enfermeiro_nome, e.coren AS enfermeiro_coren,
                   u.email AS enfermeiro_email, u.ativo AS enfermeiro_ativo
            FROM prescricao p
            LEFT JOIN enfermeiro e ON p.enfermeiro_id = e.id
            LEFT JOIN usuario u ON p.enfermeiro_id = u.id
            WHERE p.id = :id
        """
        linha = self.db.execute(sql, {"id": id_prescricao}).fetchone()

        if not linha:
            return None

        prescricao = Prescricao(
            id_prescricao=linha.id,
            nome_medicamento=linha.nome_medicamento,
            dose=linha.dose,
            intervalo_horas=linha.intervalo_horas,
            status=linha.status,
            evolucao_id=linha.evolucao_id,
            enfermeiro_id=linha.enfermeiro_id,
            data_hora_aplicacao=linha.data_hora_aplicacao
        )

        if linha.enfermeiro_id is not None:
            prescricao.enfermeiro = Enfermeiro(
                id_enfermeiro=linha.enfermeiro_id,
                nome=linha.enfermeiro_nome,
                coren=linha.enfermeiro_coren,
                email=linha.enfermeiro_email,
                ativo=bool(linha.enfermeiro_ativo)
            )

        return prescricao