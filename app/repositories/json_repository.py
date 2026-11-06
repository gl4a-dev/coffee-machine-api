import json
import os
from pathlib import Path
from threading import Lock
from typing import List, Dict, Any, Optional

from app.repositories.base_repository import ( 
    MenuRepositoryProtocol, 
    StockRepositoryProtocol, 
    StateRepositoryProtocol, 
    OrderRepositoryProtocol
)


class JsonCoffeeMachineRepository(
    MenuRepositoryProtocol, 
    StockRepositoryProtocol, 
    StateRepositoryProtocol, 
    OrderRepositoryProtocol
):
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
        with self.lock:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            os.replace(temp_path, file_path)


    # --- Menu Implementation ---
    def get_all_drinks(self) -> List[Dict[str, Any]]:
        return self._read_json("menu.json")

    def get_drink_by_id(self, drink_id: int) -> Optional[Dict[str, Any]]:
        menu = self.get_all_drinks()
        for item in menu:
            if item["id"] == drink_id:
                return item
        return None

    def update_drink_price(self, drink_id: int, new_price: float) -> None:
        menu = self.get_all_drinks()
        for item in menu:
            if item["id"] == drink_id:
                item["preco"] = new_price
                break
        self._write_json("menu.json", menu)


    # --- Stock Implementation ---
    def get_stock(self) -> Dict[str, Dict[str, Any]]:
        return self._read_json("stock.json")

    def update_stock(self, new_stock: Dict[str, Dict[str, Any]]) -> None:
        self._write_json("stock.json", new_stock)


    # --- State Implementation ---
    def get_state(self) -> Dict[str, Any]:
        return self._read_json("state.json")

    def update_state(self, new_state: Dict[str, Any]) -> None:
        self._write_json("state.json", new_state)


    # --- Order Implementation ---
    def get_all_orders(self) -> List[Dict[str, Any]]:
        return self._read_json("orders.json")
    
    def get_order_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        orders = self.get_all_orders()
        for order in orders:
            if order["id"] == order_id:
                return order
        return None
    
    def save_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        orders = self.get_all_orders()
        order["id"] = len(orders) + 1
        orders.append(order)
        self._write_json("orders.json", orders)
        return order

    def update_order(self, order_id: int, updated_data: Dict[str, Any]) -> None:
        orders = self.get_all_orders()
        for i, order in enumerate(orders):
            if order["id"] == order_id:
                orders[i] = updated_data
                break
        self._write_json("orders.json", orders)