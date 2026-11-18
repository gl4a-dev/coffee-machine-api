from fastapi import APIRouter, Depends
from app.repositories.base_repository import BaseCoffeeRepository
from app.api.deps import get_repository, verify_operator_key

router = APIRouter()

@router.get(
    "/estoque",
    summary="Consulta de reservatórios (Protegido)",
    dependencies=[Depends(verify_operator_key)]
)

def consultar_estoque(repo: BaseCoffeeRepository =
Depends(get_repository)):
    """
    Retorna os níveis atuais de cada reservatório e se há alerta de nível baixo.
    Exige que o operador clique no botão 'Authorize' no topo do Swagger e informe a OPERADOR_KEY (RN11)[cite: 5].
    """
    stock = repo.get_stock()

    reservatorios = []
    stock_dict = stock.model_dump()
    for item_nome, dados in stock_dict.items():
        reservatorios.append({
            "item": item_nome,
            "atual": dados["atual"],
            "capacidade": dados["capacidade"],
            "nivelBaixo": dados["atual"] < dados["nivel_baixo"]
        })

    return {"reservatorios": reservatorios}