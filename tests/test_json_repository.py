import pytest
from pathlib import Path

from app.data.setup import restore_setup_data
from app.repositories.json_repository import JsonCoffeeMachineRepository


@pytest.fixture
def repo(tmp_path: Path):
    restore_setup_data(tmp_path)
    return JsonCoffeeMachineRepository(tmp_path)


def test_menu_repository_operations(repo:JsonCoffeeMachineRepository):
    drinks = repo.get_all_drinks()
    assert len(drinks) == 5

    drink = repo.get_drink_by_id(1)
    assert drink is not None
    assert drink["nome"] == "Café expresso"

    assert repo.get_drink_by_id(99) is None

    
    repo.update_drink_price(1, 4.75)
    updated_drink = repo.get_drink_by_id(1)
    assert updated_drink["preco"] == 4.75


def test_stock_repository_operations(repo:JsonCoffeeMachineRepository):
    stock = repo.get_stock()
    assert "agua" in stock
    assert stock["agua"]["atual"] == 2000

    
    stock["agua"]["atual"] = 1500
    repo.update_stock(stock)

    new_stock = repo.get_stock()
    assert new_stock["agua"]["atual"] == 1500


def test_state_repository_operations(repo:JsonCoffeeMachineRepository):
    state = repo.get_state()
    assert state["estado"] == "PRONTA"
    assert state["credito"] == 0.00

    
    state["estado"] = "PREPARANDO"
    state["credito"] = 10.00
    repo.update_state(state)

    updated_state = repo.get_state()
    assert updated_state["estado"] == "PREPARANDO"
    assert updated_state["credito"] == 10.00


def test_order_repository_operations(repo:JsonCoffeeMachineRepository):
    orders = repo.get_all_orders()
    assert orders == []

    new_order = {"produto_id": 4, "acucar": 2, "status": "EM_PREPARO"}
    saved = repo.save_order(new_order)
    
    assert saved["id"] == 1
    assert len(repo.get_all_orders()) == 1


    fetched = repo.get_order_by_id(1)
    assert fetched is not None
    assert fetched["produto_id"] == 4

    assert repo.get_order_by_id(99) is None


    fetched["status"] = "CONCLUIDO"
    repo.update_order(1, fetched)

    updated_fetched = repo.get_order_by_id(1)
    assert updated_fetched["status"] == "CONCLUIDO"