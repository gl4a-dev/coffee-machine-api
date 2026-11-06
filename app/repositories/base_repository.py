from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class MenuRepositoryProtocol(ABC):
    @abstractmethod
    def get_all_drinks(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_drink_by_id(self, drink_id: int) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def update_drink_price(self, drink_id: int, new_price: float) -> None:
        pass


class StockRepositoryProtocol(ABC):
    @abstractmethod
    def get_stock(self) -> Dict[str, Dict[str, Any]]:
        pass

    @abstractmethod
    def update_stock(self, new_stock: Dict[str, Dict[str, Any]]) -> None:
        pass


class StateRepositoryProtocol(ABC):
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_state(self, new_state: Dict[str, Any]) -> None:
        pass


class OrderRepositoryProtocol(ABC):
    @abstractmethod
    def get_all_orders(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def save_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_order(self, order_id: int, updated_data: Dict[str, Any]) -> None:
        pass