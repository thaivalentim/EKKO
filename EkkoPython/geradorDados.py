import random
import time
from datetime import datetime
from pymongo import MongoClient
from faker import Faker

# 🔧 CONFIGURAÇÕES
MONGO_URI = "mongodb+srv://thaizavalentim:Lildashboard13_@testeekko2507.fmbmatr.mongodb.net/?retryWrites=true&w=majority&appName=testeEkko2507"  
NOME_DB = "EkkoDB"
QUANTIDADE_USUARIOS = 5
INTERVALO_ENVIO_SEGUNDOS = 5
NUM_ITERACOES_SENSOR = 10 

# Inicializadores
fake = Faker('pt_BR')

def conectar_mongo(uri, nome_db):
    """Estabelece conexão com o MongoDB.""" 
    try:
        client = MongoClient(uri)
        print("✅ Conexão com o MongoDB estabelecida.")
        return client[nome_db]
    except Exception as e:
        print("❌ Erro ao conectar com o MongoDB:", e)
        exit()

def gerar_usuario_fake():
    """Gera dados fictícios de um usuário."""
    return {
        "nome": fake.name(),
        "email": fake.unique.email(),
        "senha_hash": fake.sha256(),
        "papel": "cliente"
    }

def gerar_agricultor_fake(user_id):
    """Gera dados fictícios de um agricultor vinculado a um usuário."""
    return {
        "user_id": user_id,
        "nome_fazenda": fake.company(),
        "localizacao": fake.address()
    }

def gerar_leitura_solo_fake(agricultor_id):
    """Gera uma leitura pontual de solo simulada."""
    return {
        "agricultor_id": agricultor_id,
        "data_leitura": datetime.utcnow(),
        "ph": round(random.uniform(4.5, 8.5), 2),
        "umidade": round(random.uniform(10, 90), 2),
        "temperatura": round(random.uniform(10, 40), 2)
    }

def gerar_dado_sensor_continuo(agricultor_id):
    """Gera dados contínuos simulados de sensores de solo e ar."""
    return {
        "agricultor_id": agricultor_id,
        "umidade_solo": round(random.uniform(30, 70), 2),
        "temperatura_solo": round(random.uniform(15, 35), 1),
        "umidade_ar": round(random.uniform(40, 80), 2),
        "localizacao": "Estufa Experimental 1",
        "timestamp": datetime.utcnow()
    }

def simular_dados_continuos(db, agricultor_id):
    """Insere dados simulados em tempo real para um agricultor."""
    print(f"📡 Iniciando simulação de {NUM_ITERACOES_SENSOR} leituras de sensores...")
    for _ in range(NUM_ITERACOES_SENSOR):
        dado = gerar_dado_sensor_continuo(agricultor_id)
        db.leituras_solo.insert_one(dado)
        print(f"[{datetime.utcnow()}] 🌱 Dado de sensor enviado com sucesso.")
        time.sleep(INTERVALO_ENVIO_SEGUNDOS)

def main():
    db = conectar_mongo(MONGO_URI, NOME_DB)
    agricultores_ids = []

    for i in range(QUANTIDADE_USUARIOS):
        user_id = db.users.insert_one(gerar_usuario_fake()).inserted_id
        print(f"Usuário {i+1} adicionado com sucesso.")

        agricultor_id = db.agricultores.insert_one(gerar_agricultor_fake(user_id)).inserted_id
        print(f"Agricultor {i+1} adicionado com sucesso.")

        agricultores_ids.append(agricultor_id)

        for j in range(3):
            db.leituras_solo.insert_one(gerar_leitura_solo_fake(agricultor_id))
        print(f"3 leituras iniciais inseridas para agricultor {i+1}.")

    print(f"✅ {QUANTIDADE_USUARIOS} usuários e agricultores criados com leituras iniciais.")
    simular_dados_continuos(db, agricultores_ids[0])

if __name__ == "__main__":
    main()
