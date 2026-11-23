import pytest
from decimal import Decimal

from app.domain.models import MachineState, MachineStateEnum


def test_machine_state_credito_zero():
    state = MachineState(
        estado=MachineStateEnum.PRONTA,
        credito=Decimal("0.00")
    )

    assert state.credito == Decimal("0.00")


def test_machine_state_credito_valido():
    state = MachineState(
        estado=MachineStateEnum.PRONTA,
        credito=Decimal("25.00")
    )

    assert state.credito == Decimal("25.00")


def test_machine_state_credito_negativo():
    with pytest.raises(Exception):
        MachineState(
            estado=MachineStateEnum.PRONTA,
            credito=Decimal("-1.00")
        )


def test_machine_state_credito_acima_limite():
    with pytest.raises(Exception):
        MachineState(
            estado=MachineStateEnum.PRONTA,
            credito=Decimal("51.00")
        )