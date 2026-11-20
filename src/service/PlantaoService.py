from src.models.Classes import Plantao
from src.repositori.PlantaoRepository import PlantaoRepository
from src.repositori.Equipe_Medica.MedicoRepository import MedicoRepository
from src.exceptions import NaoEncontradoError, RegraDeNegocioError


class PlantaoService:

    def __init__(self, plantao_repo: PlantaoRepository, medico_repo: MedicoRepository):
        self.plantao_repo = plantao_repo
        self.medico_repo = medico_repo

    def alocar_medico_no_plantao(self, coordenador_id: int, medico_id: int, setor_ala: str,
    data_hora_inicio, data_hora_fim) -> int:

        if data_hora_inicio >= data_hora_fim:
            raise RegraDeNegocioError("A data/hora de início do plantão deve ser anterior à data/hora de fim.")

        alocar = self.medico_repo.buscar_medicos_disponiveis(data_hora_inicio, data_hora_fim)
        medicos_livres = [medico.id for medico in alocar]

        if medico_id not in medicos_livres:
            raise RegraDeNegocioError("O médico não está disponível para este horário.")

        novo_plantao = Plantao(
            id_plantao=None,
            setor_ala=setor_ala,
            data_hora_inicio=data_hora_inicio,
            data_hora_fim=data_hora_fim,
            medico_id=medico_id,
            coordenador_id=coordenador_id
        )

        return self.plantao_repo.inserir_plantao(novo_plantao)

    def atualizar_plantao(self, id_plantao: int, coordenador_id: int, medico_id: int,
    setor_ala: str, data_hora_inicio, data_hora_fim):

        self.buscar_plantao_por_id(id_plantao)

        if data_hora_inicio >= data_hora_fim:
            raise RegraDeNegocioError("A data/hora de início do plantão deve ser anterior à data/hora de fim.")

        plantao_corrigido = Plantao(
            id_plantao=id_plantao,
            coordenador_id=coordenador_id,
            medico_id=medico_id,
            setor_ala=setor_ala,
            data_hora_inicio=data_hora_inicio,
            data_hora_fim=data_hora_fim
        )
        self.plantao_repo.atualizar_plantao(plantao_corrigido)

    def buscar_plantao_por_id(self, id_plantao: int) -> Plantao:

        plantao = self.plantao_repo.buscar_por_id(id_plantao)

        if plantao is None:
            raise NaoEncontradoError("Plantão não encontrado no sistema.")

        return plantao

    def buscar_detalhes_do_plantao(self, id_plantao: int) -> Plantao:

        plantao_detalhado = self.plantao_repo.buscar_detalhes_por_id(id_plantao)

        if plantao_detalhado is None:
            raise NaoEncontradoError("Detalhes do plantão não encontrados no sistema.")

        return plantao_detalhado

    def cancelar_plantao(self, id_plantao: int):

        self.buscar_plantao_por_id(id_plantao)
        self.plantao_repo.excluir_plantao(id_plantao)