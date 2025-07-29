# Testes - Projeto EKKO

Este diretório contém os testes automatizados para a API Ekko.

## Testes Disponíveis

### test_API_perfil.py
- Testa a visualização e atualização de perfis de usuários.
- Inclui testes para atualização inválida e usuários inválidos.
- Estruturado para execução automatizada com pytest.

### test_API_register.py
- Testa o cadastro e listagem de usuários via API.

### test_API_generalData.py
- Testa endpoints gerais da API (no caso, as coleções user, agricultor e leituras_solo no Banco de Dados) para verificar respostas e status.

### test_API_invalidUser.py
- Testa o comportamento da API ao receber usuários inválidos.

### test_API_soil_readings.py
- Testa o comportamento da API ao receber dados de leitura do solo (data, pH, umidade, temperatura), tanto válidas quanto inválidas, inexistentes ou vazias.

## Como Executar os Testes

1. Certifique-se que a API está rodando localmente em `http://127.0.0.1:8000`.
2. Execute os testes com o comando:

```bash
pytest --disable-warnings -q
```

3. Verifique os resultados no terminal.

## Próximos Passos

- Adicionar mais testes para leituras de solo e outras funcionalidades.
- Integrar testes em pipeline de CI/CD.
