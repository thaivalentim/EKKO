import requests

BASE_URL = "http://127.0.0.1:8000"

def test_obter_perfil_completo_valido():
    # OBS: usar um ID válido existente no banco
    usuario_id = "6886ea99f7bd5fd37e12d77a"
    response = requests.get(f"{BASE_URL}/perfil/{usuario_id}")
    assert response.status_code == 200
    perfil = response.json()
    assert "nome" in perfil
    assert "email" in perfil
    assert "papel" in perfil
    assert "agricultor" in perfil

def test_obter_leituras_solo_valido():
    # Usar ID válido de agricultor existente no banco de dados
    agricultor_id = "68865bf678b0524f4e8ea1e9"
    response = requests.get(f"{BASE_URL}/leituras_solo/{agricultor_id}")
    assert response.status_code == 200
    leituras = response.json()
    assert isinstance(leituras, list)
    if len(leituras) > 0:
        leitura = leituras[0]
        assert "ph" in leitura
        assert "umidade" in leitura
        assert "temperatura" in leitura
        assert "data_leitura" in leitura

def test_obter_perfil_invalido():
    usuario_id = "id_invalido"
    response = requests.get(f"{BASE_URL}/perfil/{usuario_id}")
    assert response.status_code == 400 or response.status_code == 404

def test_obter_leituras_solo_invalido():
    print("Iniciando teste de leituras de solo inválido...")
    url = f"{BASE_URL}/leituras_solo/usuario_inexistente"
    response = requests.get(url)
    
    # Mostra o status real antes de fazer a asserção
    print(f"Status code recebido: {response.status_code}")
    assert response.status_code == 400 or response.status_code == 404, f"Status inesperado: {response.status_code}"

if __name__ == "__main__":
    print("Iniciando testes de perfil, agricultor e leituras de solo...")
    test_obter_perfil_completo_valido()
    test_obter_leituras_solo_valido()
    test_obter_perfil_invalido()
    test_obter_leituras_solo_invalido()
    print("Testes concluídos com sucesso.")
