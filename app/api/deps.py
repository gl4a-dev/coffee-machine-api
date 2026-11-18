import os
from pathlib import Path
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.repositories.base_repository import BaseCoffeeRepository
from app.repositories.json_repository import JsonCoffeeMachineRepository

# Diretório onde os arquivos JSON estão salvos
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def get_repository() -> BaseCoffeeRepository:
    """Fornece a instância do repositório JSON seguindo o padrão
Strategy."""
    return JsonCoffeeMachineRepository(DATA_DIR)

# Configura o esquema de segurança que ativa o botão "Authorize" no Swagger UI
security = HTTPBearer()

# Chave do operador lida da variável de ambiente OPERADOR_KEY (RN11)
OPERADOR_KEY = os.getenv("OPERADOR_KEY", "minha-chave-operador-123")

def verify_operator_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
        Valida a chave informada no botão 'Authorize' do Swagger
    comparando com a OPERADOR_KEY.
        Retorna HTTP 401 Unauthorized se a chave for inválida ou
    estiver ausente[cite: 6].
    """

    token = credentials.credentials
    if token != OPERADOR_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"erro": "NAO AUTORIZADO", "mensagem": "Chave do operador inválida ou ausente."}
        )
    return token