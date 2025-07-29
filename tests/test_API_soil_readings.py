import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="module")
def agricultor_id():
    # Criar um agricultor para testar
    payload = {
        "nome": "Agricultor Teste",
        "email": "agricultor@exemplo.com",
        "papel": "agricultor"
    }
    response = requests.post(f"{BASE_URL}/usuarios", json=payload)
    agricultor = response.json()
    return agricultor["_id"]

def test_obter_leituras_solo_validas(agricultor_id):
    response = requests.get(f"{BASE_URL}/leituras_solo/{agricultor_id}")
    print(f"Obter leituras solo válidas: status {response.status_code}, resposta: {response.json()}")
    assert response.status_code == 200

def test_obter_leituras_solo_id_invalido():
    invalid_id = "123"
    response = requests.get(f"{BASE_URL}/leituras_solo/{invalid_id}")
    print(f"Obter leituras solo com ID inválido: status {response.status_code}, resposta: {response.json()}")
    assert response.status_code == 400

def test_obter_leituras_solo_id_inexistente():
    non_existent_id = "68865db5040380e7b9e1ed88"  # Assumindo que este ID não existe
    response = requests.get(f"{BASE_URL}/leituras_solo/{non_existent_id}")
    print(f"Obter leituras solo com ID inexistente: status {response.status_code}, resposta: {response.json()}")
    assert response.status_code == 404 or response.status_code == 200  # Pode retornar 200 com lista vazia ou 404

def test_obter_leituras_solo_sem_dados(agricultor_id):
    # Testar caso onde agricultor existe mas não tem leituras de solo
    # Isso depende dos dados no banco, pode ser necessário limpar leituras para este agricultor antes do teste
    response = requests.get(f"{BASE_URL}/leituras_solo/{agricultor_id}")
    print(f"Obter leituras solo sem dados: status {response.status_code}, resposta: {response.json()}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
