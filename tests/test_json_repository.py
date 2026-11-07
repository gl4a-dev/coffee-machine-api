import pytest
from pathlib import Path
from decimal import Decimal
from datetime import datetime

from app.data.setup import restore_setup_data
from app.repositories.json_repository import JsonCoffeeMachineRepository
from app.domain.models import Drink, Stock, MachineState, Order, MachineStateEnum, OrderStatusEnum


@pytest.fixture
def repo(tmp_path: Path):
    restore_setup_data(tmp_path)
    return JsonCoffeeMachineRepository(tmp_path)


def test_repository_get_all_drinks_returns_decimal(repo:JsonCoffeeMachineRepository):
    drinks = repo.get_all_drinks()
    assert len(drinks) == 5
    assert isinstance(drinks[0].preco, Decimal)
    assert drinks[0].nome == "Café expresso"


def test_repository_get_drink_by_id(repo:JsonCoffeeMachineRepository):
    drink = repo.get_drink_by_id(2)
    assert drink is not None
    assert drink.nome == "Café longo"
    assert drink.preco == Decimal("4.50")

    assert repo.get_drink_by_id(999) is None


def test_repository_update_drink_price(repo:JsonCoffeeMachineRepository):
    repo.update_drink_price(1, Decimal("4.75"))
    updated_drink = repo.get_drink_by_id(1)
    assert updated_drink.preco == Decimal("4.75")


def test_repository_stock_operations(repo:JsonCoffeeMachineRepository):
    """Testa a leitura e atualização do estoque da máquina."""
    stock = repo.get_stock()
    assert isinstance(stock, Stock)
    assert stock.agua.atual == 2000

    stock.agua.atual = 1800
    repo.update_stock(stock)

    reloaded_stock = repo.get_stock()
    assert reloaded_stock.agua.atual == 1800


def test_repository_state_operations(repo):
    """Testa a leitura e atualização do estado e crédito da máquina com Decimal."""
    state = repo.get_state()
    assert isinstance(state, MachineState)
    assert state.estado == MachineStateEnum.PRONTA
    assert state.credito == Decimal("0.00")

    # Altera estado e crédito
    state.estado = MachineStateEnum.PREPARANDO
    state.credito = Decimal("10.00")
    repo.update_state(state)

    reloaded_state = repo.get_state()
    assert reloaded_state.estado == MachineStateEnum.PREPARANDO
    assert reloaded_state.credito == Decimal("10.00")


def test_repository_order_operations(repo):
    """Testa salvamento, listagem, busca por ID e atualização de pedidos."""
    orders = repo.get_all_orders()
    assert orders == []

    new_order = Order(
        produto_id=4,
        produto_nome="Cappuccino",
        acucar=2,
        preco=Decimal("6.50"),
        status=OrderStatusEnum.EM_PREPARO,
        previsao_termino=datetime.now()
    )

    saved_order = repo.save_order(new_order)
    assert saved_order.id == 1
    assert len(repo.get_all_orders()) == 1

    # Busca por ID
    fetched = repo.get_order_by_id(1)
    assert fetched is not None
    assert fetched.produto_nome == "Cappuccino"
    assert isinstance(fetched.preco, Decimal)

    # Atualiza status do pedido
    fetched.status = OrderStatusEnum.CONCLUIDO
    repo.update_order(1, fetched)

    updated_fetched = repo.get_order_by_id(1)
    assert updated_fetched.status == OrderStatusEnum.CONCLUIDO