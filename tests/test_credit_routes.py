from decimal import Decimal

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.deps import get_repository
from app.domain.models import MachineState, MachineStateEnum


class FakeRepository:
    def __init__(self):
        self.state = MachineState(
            estado=MachineStateEnum.PRONTA,
            credito=Decimal("0.00")
        )

    def get_state(self):
        return self.state

    def update_state(self, new_state):
        self.state = new_state


def test_post_credito_valido():
    repository = FakeRepository()

    app.dependency_overrides[get_repository] = lambda: repository

    client = TestClient(app)

    response = client.post("/credito", json={"valor": 5.00})

    assert response.status_code == 200
    assert repository.state.credito == Decimal("5.00")

    app.dependency_overrides.clear()


def test_post_credito_moeda_invalida():
    repository = FakeRepository()

    app.dependency_overrides[get_repository] = lambda: repository

    client = TestClient(app)

    response = client.post("/credito", json={"valor": 3.00})

    assert response.status_code == 400
    assert repository.state.credito == Decimal("0.00")

    app.dependency_overrides.clear()


def test_post_credito_limite_excedido():
    repository = FakeRepository()
    repository.state.credito = Decimal("40.00")

    app.dependency_overrides[get_repository] = lambda: repository

    client = TestClient(app)

    response = client.post("/credito", json={"valor": 20.00})

    assert response.status_code == 400
    assert repository.state.credito == Decimal("40.00")

    app.dependency_overrides.clear()


def test_post_troco():
    repository = FakeRepository()
    repository.state.credito = Decimal("10.00")

    app.dependency_overrides[get_repository] = lambda: repository

    client = TestClient(app)

    response = client.post("/troco")

    assert response.status_code == 200
    assert repository.state.credito == Decimal("0.00")

    app.dependency_overrides.clear()