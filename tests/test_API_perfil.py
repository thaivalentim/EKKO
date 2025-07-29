import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="module")
def usuario_id():
    # Criar um usuário para testar
    payload = {
        "nome": "Usuário Teste",
        "email": "teste@exemplo.com",
        "papel": "cliente"
    }
    response = requests.post(f"{BASE_URL}/usuarios", json=payload)
    usuario = response.json()
    return usuario["_id"]

def test_visualizar_perfil(usuario_id):
    response = requests.get(f"{BASE_URL}/perfil/{usuario_id}")
    print(f"Visualizar perfil: status {response.status_code}, resposta: {response.json()}")
    assert response.status_code == 200, f"Esperado 200, obtido {response.status_code}"

def test_atualizar_perfil(usuario_id):
    dados = {
        "nome": "Usuário Teste Atualizado",
        "email": "testeatualizado@exemplo.com",
        "papel": "admin"
    }
    response = requests.put(f"{BASE_URL}/perfil/{usuario_id}", json=dados)
    print(f"Atualizar perfil: status {response.status_code}, resposta: {response.json()}")
    assert response.status_code == 200, f"Esperado 200, obtido {response.status_code}"

def test_atualizar_perfil_invalido(usuario_id):
    dados = {}
    response = requests.put(f"{BASE_URL}/perfil/{usuario_id}", json=dados)
    print(f"Atualizar perfil inválido: status {response.status_code}, resposta: {response.json()}")
    assert response.status_code == 400, f"Esperado 400, obtido {response.status_code}"

def test_perfil_usuario_invalido():
    usuario_id = "123"
    response = requests.get(f"{BASE_URL}/perfil/{usuario_id}")
    print(f"Visualizar perfil usuário inválido: status {response.status_code}, resposta: {response.json()}")
    assert response.status_code == 400, f"Esperado 400, obtido {response.status_code}"

    response = requests.put(f"{BASE_URL}/perfil/{usuario_id}", json={"nome": "Teste"})
    print(f"Atualizar perfil usuário inválido: status {response.status_code}, resposta: {response.json()}")
    assert response.status_code == 400, f"Esperado 400, obtido {response.status_code}"
