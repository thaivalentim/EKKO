import random
import time
from datetime import datetime
from pymongo import MongoClient
from faker import Faker

# 🔧 CONFIGURAÇÕES
MONGO_URI = "mongodb+srv://thaizavalentim:Lildashboard13_@testeekko2507.fmbmatr.mongodb.net/?retryWrites=true&w=majority&appName=testeEkko2507"
NOME_DB = "EkkoDB_UnifiedUser"
QUANTIDADE_USUARIOS = 5
INTERVALO_ENVIO_SEGUNDOS = 5
NUM_ITERACOES_SENSOR = 10 

fake = Faker('pt_BR')

def conectar_mongo(uri, nome_db):
    try:
        client = MongoClient(uri)
        print("✅ Conexão com o MongoDB estabelecida.")
        return client[nome_db]
    except Exception as e:
        print("❌ Erro ao conectar com o MongoDB:", e)
        exit()

def gerar_usuario_fake():
    """Gera dados fictícios de usuário (com dados de sua fazenda incluídos)."""
    return {
        "nome": fake.name(),
        "email": fake.unique.email(),
        "senha_hash": fake.sha256(),
        "papel": "cliente",
        "nome_fazenda": fake.company(),
        "localizacao": fake.address()
    }

def gerar_leitura_solo_fake(usuario_id):
    """Gera uma leitura simulada de solo vinculada ao usuário."""
    return {
        "usuario_id": usuario_id,
        "dispositivo": "EKKO - Agro & Automação",
        "umidade": round(random.uniform(10, 90), 2),
        "temperatura": round(random.uniform(10, 40), 2), 
        "pH": round(random.uniform(4.5, 8.5), 2),
        "condutividade_eletrica": round(random.uniform(0.1, 2.0), 2),
        "salinidade": round(random.uniform(0.1, 5.0), 2), 
        "NPK": round(random.uniform(0.1, 10.0), 2),
        "data_leitura": datetime.utcnow()
    }

def gerar_dado_sensor_continuo(usuario_id, ultimo_dado=None):
    """Gera leituras simuladas contínuas com variações suaves."""
    def variar(valor, min_, max_, delta=1.5):
        novo = valor + random.uniform(-delta, delta)
        return round(max(min_, min(max_, novo)), 2)
    
    if not ultimo_dado:
        return gerar_leitura_solo_fake(usuario_id)

    return {
        "usuario_id": usuario_id,
        "dispositivo": "EKKO - Agro & Automação",
        "umidade": variar(ultimo_dado["umidade"], 10, 90),
        "temperatura": variar(ultimo_dado["temperatura"], 10, 40),
        "pH": variar(ultimo_dado["pH"], 4.5, 8.5),
        "condutividade_eletrica": variar(ultimo_dado["condutividade_eletrica"], 0.1, 2.0),
        "salinidade": variar(ultimo_dado["salinidade"], 0.1, 5.0),
        "NPK": variar(ultimo_dado["NPK"], 0.1, 10.0),
        "data_leitura": datetime.utcnow()
    }

def simular_dados_continuos(db, usuario_id):
    """Envia leituras contínuas simuladas de sensores para um usuário."""
    print(f"📡 Iniciando simulação de {NUM_ITERACOES_SENSOR} leituras contínuas...")
    ultimo = gerar_leitura_solo_fake(usuario_id)
    for _ in range(NUM_ITERACOES_SENSOR):
        dado = gerar_dado_sensor_continuo(usuario_id, ultimo)
        db.leituras_solo.insert_one(dado)
        ultimo = dado
        print(f"[{datetime.utcnow()}] 🌱 Dado contínuo enviado.")
        time.sleep(INTERVALO_ENVIO_SEGUNDOS)

def main():
    db = conectar_mongo(MONGO_URI, NOME_DB)
    usuarios_ids = []

    for i in range(QUANTIDADE_USUARIOS):
        usuario = gerar_usuario_fake()
        usuario_id = db.usuarios.insert_one(usuario).inserted_id
        print(f"👤 Usuário {i+1} criado.")

        usuarios_ids.append(usuario_id)

        for j in range(3):
            db.leituras_solo.insert_one(gerar_leitura_solo_fake(usuario_id))
        print(f"✅ Leituras iniciais para usuário {i+1} inseridas.")

    print(f"\n🌿 Simulação concluída: {QUANTIDADE_USUARIOS} usuários com dados de solo.")
    simular_dados_continuos(db, usuarios_ids[0])

if __name__ == "__main__":
    main()
