# EkkoAPI/main.py

from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from EkkoAPI.profile_management import router as profile_router
from EkkoAPI.soil_readings import router as soil_router
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
from typing import List
import os
from dotenv import load_dotenv

# Carrega variáveis do .env 
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI") or "mongodb+srv://thaizavalentim:Lildashboard13_@testeekko2507.fmbmatr.mongodb.net/?retryWrites=true&w=majority&appName=testeEkko2507"

# Conexão MongoDB
client = MongoClient(MONGO_URI)
db = client["EkkoDB_UnifiedUser"]
usuarios_collection = db["usuarios"]

# FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Ekko")

# Configuração CORS para permitir frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desenvolvimento, permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router)
app.include_router(soil_router)

# Serialização de documentos MongoDB
def serialize_user(user) -> dict:
    user["_id"] = str(user["_id"])
    return user

# Modelo de entrada
class Usuario(BaseModel):
    nome: str = Field(..., min_length=1)
    email: EmailStr
    papel: str = Field(..., min_length=1)

@app.get("/")
def root():
    return {"mensagem": "API Ekko está online!"}

@app.get("/usuarios", response_model=List[dict])
def listar_usuarios():
    try:
        usuarios = list(usuarios_collection.find())
        return [serialize_user(u) for u in usuarios]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")

@app.post("/usuarios", response_model=dict)
def criar_usuario(usuario: Usuario):
    try:
        novo = usuario.dict()
        result = usuarios_collection.insert_one(novo)
        novo["_id"] = str(result.inserted_id)
        return novo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

@app.get("/usuarios/{usuario_id}", response_model=dict)
def obter_usuario(usuario_id: str):
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return serialize_user(usuario)
    except HTTPException as http_exc:
        raise http_exc
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter usuário: {str(e)}")
