import json
from pathlib import Path

from app.data.setup import restore_setup_data


def test_restore_setup_creates_all_files_from_scratch(tmp_path:Path):
    restore_setup_data(tmp_path)
    
    expected_files = ["menu.json", "stock.json", "state.json", "orders.json"]
    
    for file_name in expected_files:
        file_path = tmp_path / file_name
        assert file_path.exists()
        assert file_path.is_file()


    with open(tmp_path / "menu.json", "r", encoding="utf-8") as f:
        menu_data = json.load(f)

    assert len(menu_data) == 5
    assert menu_data[0]["nome"] == "Café expresso"
    assert menu_data[0]["preco"] == 4.00


    with open(tmp_path / "stock.json", "r", encoding="utf-8") as f:
        stock_data = json.load(f)

    assert stock_data["agua"]["atual"] == 2000
    assert stock_data["cafe"]["atual"] == 500
    assert stock_data["copos"]["atual"] == 50


    with open(tmp_path / "state.json", "r", encoding="utf-8") as f:
        state_data = json.load(f)

    assert state_data["estado"] == "PRONTA"
    assert state_data["credito"] == 0.00
    assert state_data["contador_limpeza"] == 0


    with open(tmp_path / "orders.json", "r", encoding="utf-8") as f:
        orders_data = json.load(f)

    assert orders_data == []


def test_restore_setup_resets_modified_files(tmp_path:Path):
    state_file = tmp_path / "state.json"
    stock_file = tmp_path / "stock.json"
    
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump({"estado": "MANUTENCAO", "credito": 25.00, "contador_limpeza": 15}, f)
        
    with open(stock_file, "w", encoding="utf-8") as f:
        json.dump({"agua": {"atual": 100, "capacidade": 2000, "nivel_baixo": 400}}, f)


    restore_setup_data(tmp_path)


    with open(state_file, "r", encoding="utf-8") as f:
        state_data = json.load(f)

    assert state_data["estado"] == "PRONTA"
    assert state_data["credito"] == 0.00
    assert state_data["contador_limpeza"] == 0


    with open(stock_file, "r", encoding="utf-8") as f:
        stock_data = json.load(f)

    assert stock_data["agua"]["atual"] == 2000


def test_restore_setup_with_partial_existing_files(tmp_path:Path):
    orders_file = tmp_path / "orders.json"
    with open(orders_file, "w", encoding="utf-8") as f:
        json.dump([{"id": 999, "produto": "Pedido Antigo"}], f)

    assert not (tmp_path / "menu.json").exists()

    restore_setup_data(tmp_path)

    assert (tmp_path / "menu.json").exists()
    assert (tmp_path / "stock.json").exists()
    assert (tmp_path / "state.json").exists()
    assert (tmp_path / "orders.json").exists()

    with open(orders_file, "r", encoding="utf-8") as f:
        orders_data = json.load(f)

    assert orders_data == []