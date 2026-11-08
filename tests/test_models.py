import pytest
from datetime import datetime
from decimal import Decimal
from pydantic import ValidationError

from app.domain.models import (
    Drink,
    StockItem,
    Stock,
    MachineState,
    Order,
    MachineStateEnum,
    OrderStatusEnum,
)


def test_drink_valid_model():
    drink = Drink(
        id=1,
        nome="Café Expresso",
        agua=40,
        cafe=8,
        leite=0,
        chocolate=0,
        preparo=5,
        preco=Decimal("4.00")
    )
    assert drink.id == 1
    assert drink.preco == Decimal("4.00")
    assert drink.agua == 40


def test_drink_invalid_price():
    with pytest.raises(ValidationError):
        Drink(
            id=1,
            nome="Café Grátis",
            agua=40,
            cafe=8,
            preco=Decimal("0.00")
        )

    with pytest.raises(ValidationError):
        Drink(
            id=1,
            nome="Café Negativo",
            agua=40,
            cafe=8,
            preco=Decimal("-1.50")
        )


def test_drink_negative_ingredients_fail():
    with pytest.raises(ValidationError):
        Drink(
            id=1,
            nome="Café Inválido",
            agua=-10,
            cafe=8,
            preco=Decimal("4.00")
        )


def test_machine_state_credits_limit():
    state_valid = MachineState(estado=MachineStateEnum.PRONTA, credito=Decimal("50.00"))
    assert state_valid.credito == Decimal("50.00")

    with pytest.raises(ValidationError):
        MachineState(estado=MachineStateEnum.PRONTA, credito=Decimal("55.00"))

    with pytest.raises(ValidationError):
        MachineState(estado=MachineStateEnum.PRONTA, credito=Decimal("-0.01"))


def test_order_sugar_limits():
    valid_order = Order(
        produto_id=1,
        produto_nome="Café Expresso",
        acucar=3,
        preco=Decimal("4.00"),
        previsao_termino=datetime.now()
    )
    assert valid_order.acucar == 3

    with pytest.raises(ValidationError):
        Order(
            produto_id=1,
            produto_nome="Café Expresso",
            acucar=4,
            preco=Decimal("4.00"),
            previsao_termino=datetime.now()
        )

    with pytest.raises(ValidationError):
        Order(
            produto_id=1,
            produto_nome="Café Expresso",
            acucar=-1,
            preco=Decimal("4.00"),
            previsao_termino=datetime.now()
        )