from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal

from app.domain.models import Drink, Stock, MachineState, Order


class BaseCoffeeRepository(ABC):
    # --- Menu ---
    @abstractmethod
    def get_all_drinks(self) -> List[Drink]:
        pass

    @abstractmethod
    def get_drink_by_id(self, drink_id: int) -> Optional[Drink]:
        pass

    @abstractmethod
    def update_drink_price(self, drink_id: int, new_price: Decimal) -> None:
        pass

    # --- Stock ---
    @abstractmethod
    def get_stock(self) -> Stock:
        pass

    @abstractmethod
    def update_stock(self, new_stock: Stock) -> None:
        pass

    # --- State ---
    @abstractmethod
    def get_state(self) -> MachineState:
        pass

    @abstractmethod
    def update_state(self, new_state: MachineState) -> None:
        pass

    # --- Orders ---
    @abstractmethod
    def get_all_orders(self) -> List[Order]:
        pass
    
    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def save_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    def update_order(self, order_id: int, updated_data: Order) -> None:
        pass