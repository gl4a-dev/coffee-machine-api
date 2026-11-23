from fastapi import APIRouter, Depends
from app.repositories.base_repository import BaseCoffeeRepository
from app.api.deps import get_repository
from decimal import Decimal
from fastapi import HTTPException

from app.domain.models import CreditRequest
from app.services.credit_service import CreditService
router = APIRouter()

@router.get("/produtos", summary="Cardápio com disponibilidade")
def consultar_cardapio(repo: BaseCoffeeRepository = Depends(get_repository)):
    """
        Retorna o cardápio com preços, tempos de preparo e se cada bebida está disponível com base no estoque atual de ingredientes e copos (RN10)[cite:5].
    """

    drinks = repo.get_all_drinks()
    stock = repo.get_stock()

    cardapio = []
    for drink in drinks:
        disponivel = (
            stock.agua.atual >= drink.agua and
            stock.cafe.atual >= drink.cafe and
            stock.leite.atual >= drink.leite and
            stock.chocolate.atual >= drink.chocolate and
            stock.copos.atual >= 1
        )
        cardapio.append({
            "id": drink.id,
            "nome": drink.nome,
            "preco": float(drink.preco),
            "preparo": drink.preparo,
            "disponivel": disponivel
            })
    return cardapio

@router.get("/status", summary="Estado atual e crédito")
def consultar_status(repo: BaseCoffeeRepository = Depends(get_repository)):
    """Retorna o estado operacional atual da máquina e o crédito acumulado."""
    state = repo.get_state()
    return {
        "estado": state.estado,
        "credito": float(state.credito)
    }


@router.post("/credito", summary="Inserir crédito na máquina")
def inserir_credito(
    request: CreditRequest,
    repo: BaseCoffeeRepository = Depends(get_repository)
):
    service = CreditService(repo)

    novo_credito = service.inserir_credito(request.valor)

    return {
        "mensagem": "Crédito inserido com sucesso.",
        "credito": float(novo_credito)
    }


@router.post("/troco", summary="Devolver crédito restante")
def solicitar_troco(
    repo: BaseCoffeeRepository = Depends(get_repository)
):
    service = CreditService(repo)

    valor_troco = service.devolver_troco()

    return {
        "mensagem": "Troco devolvido com sucesso.",
        "troco": float(valor_troco)
    }
