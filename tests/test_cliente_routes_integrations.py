from fastapi.testclient import TestClient

from app.api.main import app
from app.api.deps import get_repository
from app.repositories.json_repository import JsonCoffeeMachineRepository
from app.data.setup import restore_setup_data


def test_consultar_menu(tmp_path):
    restore_setup_data(tmp_path)
    repository = JsonCoffeeMachineRepository(tmp_path)

    app.dependency_overrides[get_repository] = lambda: repository

    client = TestClient(app)

    response = client.get("/produtos")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5

    app.dependency_overrides.clear()


def test_consultar_estado_maquina(tmp_path):
    restore_setup_data(tmp_path)
    repository = JsonCoffeeMachineRepository(tmp_path)

    app.dependency_overrides[get_repository] = lambda: repository

    client = TestClient(app)

    response = client.get("/status")

    assert response.status_code == 200
    assert response.json()["estado"] == "PRONTA"
    assert response.json()["credito"] == 0.0

    app.dependency_overrides.clear()