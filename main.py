from fastapi import FastAPI
from src.routers import api_router

app = FastAPI(
    title="Sistema de Gestão Hospitalar",
    description="API completa para gestão de equipe médica, recepção, fila de prioridade e prontuários.",
    version="1.0.0"
)

app.include_router(api_router)

@app.get("/", tags=["Health Check"])
def status_servidor():
    return {"status": "online", "mensagem": "API do Hospital operando normalmente!"}