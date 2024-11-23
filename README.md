# bookron

Cadastre seus livros e tenha uma visão cronológica da sua estante.
<br>

## Instruções para execução do projeto
## Pre-requisitos:
- repositório clonado <br>
- postgresql e dbeaver (ou outro SGBD)
- python e pip instalados
<br>

1. Acesse a pasta -> `cd bookron`
2. Execute o comando para instalação das dependências -> `pip install -r requirements.txt`
3. Execute o comando para rodar o servidor -> `uvicorn app.main:app --reload`
    - Por padrão o servidor irá utilizar a porta 8000, mas é possível alterar passando uma outra porta através da flag --port, por exemplo -> `uvicorn app.main:app --port 8080 --reload`
    - A documentação da API, gerada automaticamente pelo FastAPI, poderá ser consultada acessando o endpoint `localhost:8000/docs`, nela é possível verificar todos os endpoints disponíveis

### Testes

Foi utilizada a biblioteca [Scanapi](https://scanapi.dev/) para os testes unitários dos endpoints, abaixo estão as instruções para executar os testes

1. Suba o servidor uvicorn
2. Acesse a pasta -> `cd app/tests/`
3. Execute o comando -> `scanapi run` ou `scanapi run --no-report` para desabilitar a geração do relatório HTML

### Tecnologias utilizadas
- Python 3.10
- FastAPI
- Uvicorn
- PostgreSQL
- Swagger
- ScanAPI