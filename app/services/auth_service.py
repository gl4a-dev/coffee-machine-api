
import os

from fastapi import HTTPException, status


class AuthService:

    def autenticar(self, usuario: str, senha: str) -> str:

        operador_usuario = os.getenv("OPERADOR_USUARIO")
        operador_senha = os.getenv("OPERADOR_SENHA")
        operador_key = os.getenv(
            "OPERADOR_KEY",
            "minha-chave-operador-123"
        )

        if (
            not operador_usuario
            or not operador_senha
            or usuario != operador_usuario
            or senha != operador_senha
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "erro": "CREDENCIAIS_INVALIDAS",
                    "mensagem": "Usuário ou senha inválidos."
                }
            )

        return operador_key
