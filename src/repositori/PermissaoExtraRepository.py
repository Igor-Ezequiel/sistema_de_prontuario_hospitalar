from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import Any

class PermissaoExtraRepository:

    def __init__(self, db_conexao):
        self.db = db_conexao

    def inserir_permissao(self, atendimento_id: int, medico_id: int, coordenador_id: int, motivo: str) -> int:
        sql = ("""
            INSERT INTO permissao_extra (data_hora_liberacao, motivo, validade, medico_id, atendimento_id, coordenador_id)
            VALUES (:data_hora_liberacao, :motivo, :validade, :medico_id, :atendimento_id, :coordenador_id)
            RETURNING id
        """)

        agora = datetime.now()
        resultado = self.db.execute(sql, {
            "data_hora_liberacao": agora,
            "motivo": motivo,
            "validade": agora + timedelta(hours=24),
            "medico_id": medico_id,
            "atendimento_id": atendimento_id,
            "coordenador_id": coordenador_id
        }).fetchone()

        self.db.commit()
        return resultado.id

    def buscar_permissoes_por_atendimento(self, atendimento_id: int) -> list[Any]:
        sql = ("""
            SELECT id, data_hora_liberacao, motivo, validade, medico_id, atendimento_id, coordenador_id
            FROM permissao_extra
            WHERE atendimento_id = :atendimento_id
        """)

        linhas = self.db.execute(sql, {"atendimento_id": atendimento_id}).fetchall()
        permissoes = []

        for linha in linhas:
            objeto = SimpleNamespace(
                id=linha.id,
                data_hora_liberacao=linha.data_hora_liberacao,
                motivo=linha.motivo,
                validade=linha.validade,
                medico_id=linha.medico_id,
                atendimento_id=linha.atendimento_id,
                coordenador_id=linha.coordenador_id
            )
            permissoes.append(objeto)

        return permissoes