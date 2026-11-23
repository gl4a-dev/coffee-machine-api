import pytest
from fastapi.testclient import TestClient

from app.api.main import app
from app.api.deps import get_repository, verify_operator_key
from app.repositories.json_repository import JsonCoffeeMachineRepository
from app.data.setup import restore_setup_data


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.api.deps.OPERADOR_KEY",
        "token-teste"
    )

    restore_setup_data(tmp_path)
    repository = JsonCoffeeMachineRepository(tmp_path)

    app.dependency_overrides[get_repository] = lambda: repository

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_endpoint_operador_sem_token(client):
    response = client.get("/operador/estoque")

    assert response.status_code == 401


def test_endpoint_operador_token_invalido(client):
    response = client.get(
        "/operador/estoque",
        headers={"Authorization": "Bearer token-invalido"}
    )

    assert response.status_code == 401


def test_endpoint_operador_token_valido(client):
    response = client.get(
        "/operador/estoque",
        headers={"Authorization": "Bearer token-teste"}
    )

    assert response.status_code == 200
    assert "reservatorios" in response.json()