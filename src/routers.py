from fastapi import APIRouter

from src.controllers.usuario_controller import router as usuario_router
from src.controllers.medico_controller import router as medico_router
from src.controllers.enfermeiro_controller import router as enfermeiro_router
from src.controllers.coordenador_controller import router as coordenador_router
from src.controllers.paciente_controller import router as paciente_router
from src.controllers.plantao_controller import router as plantao_router
from src.controllers.atendimento_controller import router as atendimento_router
from src.controllers.triagem_controller import router as triagem_router
from src.controllers.evolucao_controller import router as evolucao_router
from src.controllers.prescricao_controller import router as prescricao_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(usuario_router)
api_router.include_router(medico_router)
api_router.include_router(enfermeiro_router)
api_router.include_router(coordenador_router)
api_router.include_router(paciente_router)
api_router.include_router(plantao_router)
api_router.include_router(atendimento_router)
api_router.include_router(triagem_router)
api_router.include_router(evolucao_router)
api_router.include_router(prescricao_router)