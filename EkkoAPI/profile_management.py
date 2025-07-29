from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from EkkoAPI.soil_readings import router as soil_router
from datetime import datetime

# Carrega variáveis do .env 
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI") or "mongodb+srv://thaizavalentim:Lildashboard13_@testeekko2507.fmbmatr.mongodb.net/?retryWrites=true&w=majority&appName=testeEkko2507"

# Conexão MongoDB
client = MongoClient(MONGO_URI)
db = client["EkkoDB_UnifiedUser"]
usuarios_collection = db["usuarios"]

router = APIRouter()

# Modelo para atualização de usuário
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    papel: Optional[str] = Field(None, min_length=1)

# Serialização de documentos MongoDB
def serialize_user(user) -> dict:
    user["_id"] = str(user["_id"])
    return user

def serialize_farmer(farmer) -> dict:
    farmer["_id"] = str(farmer["_id"])
    farmer["user_id"] = str(farmer["user_id"])
    return farmer

@router.get("/perfil/{usuario_id}", response_model=dict)
def visualizar_perfil(usuario_id: str):
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        perfil = serialize_user(usuario)

        # Buscar leituras de solo associadas ao usuário
        soil_collection = db["leituras_solo"]
        leituras = list(soil_collection.find({"usuario_id": ObjectId(usuario_id)}))
        for leitura in leituras:
            leitura["_id"] = str(leitura["_id"])
            leitura["usuario_id"] = str(leitura["usuario_id"])
            # Formatar data_leitura se timestamp presente
            timestamp = leitura.get("timestamp") or leitura.get("data_leitura")
            if timestamp and hasattr(timestamp, "isoformat"):
                leitura["data_leitura"] = timestamp.isoformat()
            elif isinstance(timestamp, str):
                try:
                    dt = datetime.fromisoformat(timestamp)
                    leitura["data_leitura"] = dt.isoformat()
                except Exception:
                    leitura["data_leitura"] = ""
            else:
                leitura["data_leitura"] = ""
            # Ajustar nomes alternativos de campos
            leitura["umidade"] = leitura.get("umidade_solo", leitura.get("umidade", 0))
            leitura["temperatura"] = leitura.get("temperatura_solo", leitura.get("temperatura", 0))
            leitura["ph"] = leitura.get("pH", leitura.get("ph", 0))
            leitura["condutividade_eletrica"] = leitura.get("condutividade_eletrica", 0)
            leitura["dispositivo"] = leitura.get("dispositivo", "")
            leitura["salinidade"] = leitura.get("salinidade", 0)
            leitura["NPK"] = leitura.get("NPK", 0)

        perfil["leituras_solo"] = leituras

        return perfil
    except HTTPException as http_exc:
        raise http_exc
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter perfil: {str(e)}")

@router.put("/perfil/{usuario_id}", response_model=dict)
def atualizar_perfil(usuario_id: str, dados: UsuarioUpdate):
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        update_data = {k: v for k, v in dados.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")
        result = usuarios_collection.update_one({"_id": ObjectId(usuario_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        return serialize_user(usuario)
    except HTTPException as http_exc:
        raise http_exc
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar perfil: {str(e)}")
