# EkkoAPI/testeAPI_erros.py

import requests

BASE_URL = "http://127.0.0.1:8000"

def test_criar_usuario_invalido():
    """Tenta criar usuário com dados inválidos e espera erro 422"""
    payloads = [
        {},  # totalmente vazio
        {"nome": "", "email": "email@exemplo.com", "papel": "cliente"},  # nome vazio
        {"nome": "Nome", "email": "emailinvalido", "papel": "cliente"},  # email inválido
        {"nome": "Nome", "email": "email@exemplo.com", "papel": ""},  # papel vazio
    ]
    for i, payload in enumerate(payloads):
        response = requests.post(f"{BASE_URL}/usuarios", json=payload)
        print(f"Teste {i+1} criar usuário inválido: status {response.status_code}, resposta: {response.text}")
        assert response.status_code == 422, f"Esperado 422, obtido {response.status_code}"

def test_obter_usuario_invalido():
    """Tenta obter usuário com ID inválido e inexistente"""
    invalid_ids = ["123", "abc", "000000000000000000000000"]
    for i, uid in enumerate(invalid_ids):
        response = requests.get(f"{BASE_URL}/usuarios/{uid}")
        print(f"Teste {i+1} obter usuário inválido: status {response.status_code}, resposta: {response.text}")
        assert response.status_code in [400, 404], f"Esperado 400 ou 404, obtido {response.status_code}"

if __name__ == "__main__":
    print("\n🔧 Iniciando testes de erros da API...\n")
    test_criar_usuario_invalido()
    print("\n---\n")
    test_obter_usuario_invalido()
    print("\n✅ Testes de erros concluídos.")
