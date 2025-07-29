# EkkoAPI - Projeto EKKO

Este diretório contém a API desenvolvida em Python com FastAPI, que serve como interface entre o backend e o frontend, facilitando a comunicação e o fluxo de dados.

## Funcionalidades Implementadas

- Endpoints para gerenciamento de perfis de usuários (clientes e agricultores).
- Endpoints para obtenção de leituras de solo associadas aos agricultores.
- Serialização aprimorada para lidar com dados ausentes ou inválidos, evitando valores zero incorretos e datas inválidas.
- Configuração de CORS para permitir acesso do frontend local.

## Tecnologias Utilizadas

- Python 3.x
- FastAPI
- Pydantic
- MongoDB (via PyMongo)
- dotenv para variáveis de ambiente

## Como Executar

1. Configure a variável de ambiente `MONGO_URI` com a string de conexão do MongoDB.
2. Instale as dependências do projeto (recomenda-se usar um ambiente virtual).
3. Execute o servidor com:

```bash
uvicorn EkkoAPI.main:app --host 127.0.0.1 --port 8000 --reload
```

4. A API estará disponível em `http://127.0.0.1:8000`.

## Endpoints Principais

- `GET /perfil/{usuario_id}`: Retorna o perfil do usuário com dados do agricultor aninhados.
- `PUT /perfil/{usuario_id}`: Atualiza dados do perfil do usuário.
- `GET /leituras_solo/{agricultor_id}`: Retorna as leituras de solo do agricultor.

## Próximos Passos

- Implementar autenticação e autorização.
- Expandir funcionalidades da API para incluir diagnósticos de solo com IA.
- Melhorar testes automatizados e cobertura.
