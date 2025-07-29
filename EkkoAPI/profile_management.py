from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from EkkoAPI.soil_readings import router as soil_router

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
