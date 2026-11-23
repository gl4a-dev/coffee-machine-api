import pytest

from app.services.auth_service import AuthService


def test_login_operador_valido(monkeypatch):
    monkeypatch.setenv("OPERADOR_USUARIO", "operador")
    monkeypatch.setenv("OPERADOR_SENHA", "senha-local")
    monkeypatch.setenv("OPERADOR_KEY", "token-teste")

    service = AuthService()

    resultado = service.autenticar("operador", "senha-local")

    assert resultado == "token-teste"


def test_login_usuario_invalido(monkeypatch):
    monkeypatch.setenv("OPERADOR_USUARIO", "operador")
    monkeypatch.setenv("OPERADOR_SENHA", "senha-local")
    monkeypatch.setenv("OPERADOR_KEY", "token-teste")

    service = AuthService()

    with pytest.raises(Exception):
        service.autenticar("usuario-errado", "senha-local")


def test_login_senha_invalida(monkeypatch):
    monkeypatch.setenv("OPERADOR_USUARIO", "operador")
    monkeypatch.setenv("OPERADOR_SENHA", "senha-local")
    monkeypatch.setenv("OPERADOR_KEY", "token-teste")

    service = AuthService()

    with pytest.raises(Exception):
        service.autenticar("operador", "senha-errada")