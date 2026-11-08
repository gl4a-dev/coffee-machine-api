import json
import os
from pathlib import Path
from threading import Lock
from typing import List, Optional, Any
from decimal import Decimal

from app.repositories.base_repository import BaseCoffeeRepository
from app.domain.models import Drink, Stock, MachineState, Order


class JsonCoffeeMachineRepository(BaseCoffeeRepository):
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.lock = Lock()

    def _read_json(self, filename: str) -> Any:
        file_path = self.data_dir / filename
        with self.lock:
            if not file_path.exists():
                return [] if "orders" in filename else {}
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)

    def _write_json(self, filename: str, data: Any) -> None:
        file_path = self.data_dir / filename
        temp_path = file_path.with_suffix(".tmp")
        
        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return str(obj)
            raise TypeError(f"Type {type(obj)} not serializable")

        with self.lock:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, default=decimal_default, ensure_ascii=False, indent=4)
            os.replace(temp_path, file_path)

    # --- Menu Implementation ---
    def get_all_drinks(self) -> List[Drink]:
        raw_data = self._read_json("menu.json")
        return [Drink(**item) for item in raw_data]

    def get_drink_by_id(self, drink_id: int) -> Optional[Drink]:
        drinks = self.get_all_drinks()
        for drink in drinks:
            if drink.id == drink_id:
                return drink
        return None

    def update_drink_price(self, drink_id: int, new_price: Decimal) -> None:
        raw_data = self._read_json("menu.json")
        for item in raw_data:
            if item["id"] == drink_id:
                item["preco"] = str(new_price)
                break
        self._write_json("menu.json", raw_data)

    # --- Stock Implementation ---
    def get_stock(self) -> Stock:
        raw_data = self._read_json("stock.json")
        return Stock(**raw_data)

    def update_stock(self, new_stock: Stock) -> None:
        self._write_json("stock.json", new_stock.model_dump(mode="json"))

    # --- State Implementation ---
    def get_state(self) -> MachineState:
        raw_data = self._read_json("state.json")
        return MachineState(**raw_data)

    def update_state(self, new_state: MachineState) -> None:
        self._write_json("state.json", new_state.model_dump(mode="json"))

    # --- Order Implementation ---
    def get_all_orders(self) -> List[Order]:
        raw_data = self._read_json("orders.json")
        return [Order(**item) for item in raw_data]
    
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        orders = self.get_all_orders()
        for order in orders:
            if order.id == order_id:
                return order
        return None
    
    def save_order(self, order: Order) -> Order:
        orders_raw:List = self._read_json("orders.json")
        order.id = len(orders_raw) + 1
        
        orders_raw.append(order.model_dump(mode="json"))
        self._write_json("orders.json", orders_raw)
        return order

    def update_order(self, order_id: int, updated_data: Order) -> None:
        orders_raw = self._read_json("orders.json")
        for i, item in enumerate(orders_raw):
            if item["id"] == order_id:
                orders_raw[i] = updated_data.model_dump(mode="json")
                break
        self._write_json("orders.json", orders_raw)