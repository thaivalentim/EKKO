import requests

# URL base da sua API local
BASE_URL = "http://127.0.0.1:8000"

def test_criar_usuario():
    """Cria um novo usuário via POST /usuarios"""
    payload = {
        "nome": "João Silva",
        "email": "joao@teste.com",
        "papel": "cliente"
    }
    response = requests.post(f"{BASE_URL}/usuarios", json=payload)
    print("🟢 Usuário criado:", response.json())
    return response.json()

def test_listar_usuarios():
    """Lista todos os usuários via GET /usuarios"""
    response = requests.get(f"{BASE_URL}/usuarios")
    print("📋 Lista de usuários:")
    for u in response.json():
        print(" -", u)

def test_obter_usuario():
    """Obtém um usuário específico via GET /usuarios/{id}"""
    # Create a user first to get a valid ID
    user = test_criar_usuario()
    usuario_id = user["_id"]
    response = requests.get(f"{BASE_URL}/usuarios/{usuario_id}")
    print("🔍 Usuário encontrado:", response.json())

# Execução principal
if __name__ == "__main__":
    print("\n🔧 Iniciando testes da API...\n")
    test_criar_usuario()
    print("\n---\n")
    test_listar_usuarios()
    print("\n---\n")
    test_obter_usuario()
    print("\n✅ Testes concluídos.")
