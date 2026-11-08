from enum import Enum
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class MachineStateEnum(str, Enum):
    PRONTA = "PRONTA"
    PREPARANDO = "PREPARANDO"
    AGUARDANDO_LIMPEZA = "AGUARDANDO_LIMPEZA"
    MANUTENCAO = "MANUTENCAO"


class OrderStatusEnum(str, Enum):
    EM_PREPARO = "EM_PREPARO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"


class Drink(BaseModel):
    id: int
    nome: str
    agua: int = Field(default=0, ge=0)
    cafe: int = Field(default=0, ge=0)
    leite: int = Field(default=0, ge=0)
    chocolate: int = Field(default=0, ge=0)
    preparo: int = Field(default=0, ge=0)
    preco: Decimal = Field(..., ge=Decimal("0.01"))

    model_config = ConfigDict(arbitrary_types_allowed=True)


class StockItem(BaseModel):
    atual: float
    capacidade: float
    nivel_baixo: float


class Stock(BaseModel):
    agua: StockItem
    cafe: StockItem
    leite: StockItem
    chocolate: StockItem
    acucar: StockItem
    copos: StockItem


class MachineState(BaseModel):
    estado: MachineStateEnum
    credito: Decimal = Field(default=Decimal("0.00"), ge=Decimal("0.00"), le=Decimal("50.00"))
    contador_limpeza: int = Field(default=0)
    previsao_termino: Optional[datetime] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Order(BaseModel):
    id: Optional[int] = None
    produto_id: int
    produto_nome: str
    acucar: int = Field(default=0, ge=0, le=3)
    preco: Decimal
    status: OrderStatusEnum = OrderStatusEnum.EM_PREPARO
    previsao_termino: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)