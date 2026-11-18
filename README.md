# coffee-machine-api
Projeto da Disciplina ACH2006 - Engenharia de Sistemas de Informação, ministrada na EACH-USP.

Aplicação de conhecimentos e técnicas de Engenharia de Software na construção de uma API REST que simule uma máquina de café, tendo seus requisitos bem definidos.

## Setup

### Ambiente Virtual
Crie e ative um ambiente virtual na raiz do projeto:

* Ubuntu
```bash
python3 -m venv .venv
source .venv/bin/activate
```

* PowerShell
```bash
python -m venv .venv
.venv/Scripts/activate
```

### Dependências
Instale as dependências e bibliotecas utilizadas no projeto.

```bash
pip install -r requirements.txt
```

### Executando a API
Inicie o servidor local com o Uvicorn a partir da raiz do projeto:

```bash
uvicorn app.api.main:app --reload
```

Com o servidor rodando, acesse a documentação interativa (Swagger UI) no navegador em:
http://127.0.0.1:8000/docs

### Autenticação do Operador (RN11)
As rotas administrativas (/operador/...) exigem autenticação via token (HTTPBearer) validado pela variável de ambiente OPERADOR_KEY.

* Usando a chave padrão: Se nenhuma variável de ambiente for definida, a API utiliza a chave padrão minha-chave-operador-123.

* Definindo uma chave personalizada: Antes de rodar o uvicorn, defina a variável no terminal:

    * Linux / macOS: export OPERADOR_KEY="sua-chave-secreta"
    * Windows (PowerShell): $env:OPERADOR_KEY="sua-chave-secreta"   

Para testar no Swagger UI, clique no botão Authorize no topo da página e insira o valor da chave.

### Testes Automatizados
Para executar toda a suíte de testes unitários e de integração com o pytest:

```bash
pytest
```

Para verificar a porcentagem de cobertura de código (meta mínima de 75% do projeto):

```bash
pytest --cov=app
```
