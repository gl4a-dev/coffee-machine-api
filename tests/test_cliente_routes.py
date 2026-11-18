import pytest
from fastapi.testclient import TestClient
from app.api.main import app
from app.api.deps import get_repository
from app.repositories.json_repository import JsonCoffeeMachineRepository
from app.data.setup import restore_setup_data


@pytest.fixture
def client(tmp_path):
    """Cria um cliente de teste usando um diretório temporário isolado para os JSONs."""
    restore_setup_data(tmp_path)
    repo = JsonCoffeeMachineRepository(tmp_path)
    
    # Sobrescreve a dependência do repositório para não sujar os arquivos reais em app/data
    app.dependency_overrides[get_repository] = lambda: repo
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()


def test_consultar_cardapio_sucesso(client):
    """Deve retornar HTTP 200 e a lista com as 5 bebidas disponíveis (RN10)."""
    response = client.get("/produtos")
    assert response.status_code == 200
    
    dados = response.json()
    assert len(dados) == 5
    assert dados[0]["nome"] == "Café expresso"
    assert dados[0]["preco"] == 4.0
    assert dados[0]["disponivel"] is True


def test_consultar_status_inicial(client):
    """Deve retornar HTTP 200 com estado PRONTA e crédito zerado."""
    response = client.get("/status")
    assert response.status_code == 200
    
    dados = response.json()
    assert dados["estado"] == "PRONTA"
    assert dados["credito"] == 0.0