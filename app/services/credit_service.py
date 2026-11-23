
from decimal import Decimal

from fastapi import HTTPException

from app.repositories.base_repository import BaseCoffeeRepository


MOEDAS_ACEITAS = {
    Decimal("0.50"),
    Decimal("1.00"),
    Decimal("2.00"),
    Decimal("5.00"),
    Decimal("10.00"),
    Decimal("20.00"),
}

LIMITE_CREDITO = Decimal("50.00")


class CreditService:

    def __init__(self, repo: BaseCoffeeRepository):
        self.repo = repo

    def inserir_credito(self, valor: Decimal) -> Decimal:

        # 1. Validar moeda
        if valor not in MOEDAS_ACEITAS:
            raise HTTPException(
                status_code=400,
                detail={
                    "erro": "MOEDA_INVALIDA",
                    "mensagem": "Valor de moeda não aceito."
                }
            )

        # 2. Consultar estado atual
        state = self.repo.get_state()

        # 3. Verificar limite
        novo_credito = state.credito + valor

        if novo_credito > LIMITE_CREDITO:
            raise HTTPException(
                status_code=400,
                detail={
                    "erro": "LIMITE_CREDITO_EXCEDIDO",
                    "mensagem": "O crédito acumulado não pode ultrapassar R$ 50,00."
                }
            )

        # 4. Atualizar crédito
        state.credito = novo_credito

        # 5. Persistir
        self.repo.update_state(state)

        return novo_credito

    def devolver_troco(self) -> Decimal:

        # 1. Consultar estado atual
        state = self.repo.get_state()

        # 2. Guardar o valor a devolver
        valor_troco = state.credito

        # 3. Zerar crédito
        state.credito = Decimal("0.00")

        # 4. Persistir
        self.repo.update_state(state)

        return valor_troco
