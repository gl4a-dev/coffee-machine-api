from fastapi import FastAPI
from pathlib import Path

from app.data.setup import restore_setup_data
from app.api.routes import cliente_routes, operador_routes

app = FastAPI(
    title="API REST - Máquina de Café (ESI)",
    description="Backend de uma máquina de café automática desenvolvida em FastAPI.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    """Garante que os arquivos JSON de dados estejam criados e
    íntegros ao iniciar a API."""
    data_dir = Path(__file__).resolve().parent.parent / "data"
    restore_setup_data(data_dir)

# Registro dos grupos de rotas (Routers)
app.include_router(cliente_routes.router, prefix="", tags=["Cliente/ Público"])
app.include_router(operador_routes.router, prefix="/operador",
tags=["Operador (Protegido)"])