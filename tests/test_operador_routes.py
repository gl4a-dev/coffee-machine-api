import pytest
from fastapi.testclient import TestClient
from app.api.main import app
from app.api.deps import get_repository, OPERADOR_KEY
from app.repositories.json_repository import JsonCoffeeMachineRepository
from app.data.setup import restore_setup_data


@pytest.fixture
def client(tmp_path):
    """Cria um cliente de teste usando um diretório temporário isolado para os JSONs."""
    restore_setup_data(tmp_path)
    repo = JsonCoffeeMachineRepository(tmp_path)
    
    app.dependency_overrides[get_repository] = lambda: repo
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()


def test_consultar_estoque_sem_token_retorna_401(client):
    """Deve bloquear o acesso se o cabeçalho Authorization não for enviado (RN11)."""
    response = client.get("/operador/estoque")
    assert response.status_code == 401


def test_consultar_estoque_token_invalido_retorna_401(client):
    """Deve retornar HTTP 401 se o token informado estiver incorreto (RN11)."""
    headers = {"Authorization": "Bearer chave-errada-123"}
    response = client.get("/operador/estoque", headers=headers)
    
    assert response.status_code == 401
    assert response.json()["detail"]["erro"] == "NAO AUTORIZADO"


def test_consultar_estoque_com_token_valido_sucesso(client):
    """Deve retornar HTTP 200 e os 6 reservatórios cheios ao informar a OPERADOR_KEY."""
    headers = {"Authorization": f"Bearer {OPERADOR_KEY}"}
    response = client.get("/operador/estoque", headers=headers)
    
    assert response.status_code == 200
    dados = response.json()
    
    assert "reservatorios" in dados
    assert len(dados["reservatorios"]) == 6
    
    # Verifica se a água foi inicializada na capacidade máxima e sem alerta
    agua = next(item for item in dados["reservatorios"] if item["item"] == "agua")
    assert agua["atual"] == 2000
    assert agua["capacidade"] == 2000
    assert agua["nivelBaixo"] is False