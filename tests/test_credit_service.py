from decimal import Decimal

import pytest

from app.services.credit_service import CreditService
from app.domain.models import MachineState, MachineStateEnum


class FakeRepository:
    """
    Repositório falso utilizado para testar o CreditService
    sem depender dos arquivos JSON.
    """

    def __init__(self, credito_inicial=Decimal("0.00")):
        self.state = MachineState(
            estado=MachineStateEnum.PRONTA,
            credito=credito_inicial
        )

    def get_state(self):
        return self.state

    def update_state(self, new_state):
        self.state = new_state


@pytest.fixture
def repository():
    return FakeRepository()


@pytest.fixture
def credit_service(repository):
    return CreditService(repository)


def test_inserir_credito_valido(credit_service, repository):
    resultado = credit_service.inserir_credito(Decimal("5.00"))

    assert resultado == Decimal("5.00")
    assert repository.get_state().credito == Decimal("5.00")


def test_inserir_credito_com_saldo_acumulado(credit_service, repository):
    repository.state.credito = Decimal("10.00")

    resultado = credit_service.inserir_credito(Decimal("5.00"))

    assert resultado == Decimal("15.00")
    assert repository.get_state().credito == Decimal("15.00")


def test_inserir_credito_atingindo_limite(credit_service, repository):
    repository.state.credito = Decimal("30.00")

    resultado = credit_service.inserir_credito(Decimal("20.00"))

    assert resultado == Decimal("50.00")
    assert repository.get_state().credito == Decimal("50.00")


def test_inserir_credito_ultrapassando_limite(credit_service, repository):
    repository.state.credito = Decimal("40.00")

    with pytest.raises(Exception):
        credit_service.inserir_credito(Decimal("20.00"))

    assert repository.get_state().credito == Decimal("40.00")


def test_inserir_moeda_invalida(credit_service, repository):
    with pytest.raises(Exception):
        credit_service.inserir_credito(Decimal("3.00"))

    assert repository.get_state().credito == Decimal("0.00")


def test_devolver_troco(credit_service, repository):
    repository.state.credito = Decimal("12.50")

    resultado = credit_service.devolver_troco()

    assert resultado == Decimal("12.50")
    assert repository.get_state().credito == Decimal("0.00")


def test_devolver_troco_sem_credito(credit_service, repository):
    resultado = credit_service.devolver_troco()

    assert resultado == Decimal("0.00")
    assert repository.get_state().credito == Decimal("0.00")