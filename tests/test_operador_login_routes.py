from fastapi.testclient import TestClient

from app.api.main import app


def test_login_operador_valido(monkeypatch):
    monkeypatch.setenv("OPERADOR_USUARIO", "operador")
    monkeypatch.setenv("OPERADOR_SENHA", "123456")
    monkeypatch.setenv("OPERADOR_KEY", "token-teste")

    client = TestClient(app)

    response = client.post(
        "/operador/login",
        json={
            "usuario": "operador",
            "senha": "123456"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_login_operador_invalido(monkeypatch):
    monkeypatch.setenv("OPERADOR_USUARIO", "operador")
    monkeypatch.setenv("OPERADOR_SENHA", "123456")
    monkeypatch.setenv("OPERADOR_KEY", "token-teste")

    client = TestClient(app)

    response = client.post(
        "/operador/login",
        json={
            "usuario": "errado",
            "senha": "errada"
        }
    )

    assert response.status_code == 401


def test_login_operador_sem_dados():
    client = TestClient(app)

    response = client.post(
        "/operador/login",
        json={}
    )

    assert response.status_code == 422