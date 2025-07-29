from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from bson.errors import InvalidId
from typing import List
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI") or "mongodb+srv://thaizavalentim:Lildashboard13_@testeekko2507.fmbmatr.mongodb.net/?retryWrites=true&w=majority&appName=testeEkko2507"

client = MongoClient(MONGO_URI)
db = client["EkkoDB"]
soil_collection = db["leituras_solo"]
farmers_collection = db["agricultores"]

router = APIRouter()

class LeituraSolo(BaseModel):
    data_leitura: str
    ph: float = Field(0, ge=0)
    umidade: float = Field(..., ge=0)
    temperatura: float = Field(...)

from datetime import datetime

def serialize_soil_reading(reading) -> dict:
    reading["_id"] = str(reading["_id"])
    reading["agricultor_id"] = str(reading["agricultor_id"])

    # Handle timestamp conversion safely
    timestamp = reading.get("timestamp")
    if timestamp and hasattr(timestamp, "isoformat"):
        reading["data_leitura"] = timestamp.isoformat()
    elif isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp)
            reading["data_leitura"] = dt.isoformat()
        except Exception:
            reading["data_leitura"] = ""
    else:
        reading["data_leitura"] = ""

    # Use alternative field names if present
    reading["umidade"] = reading.get("umidade_solo", reading.get("umidade", 0))
    reading["temperatura"] = reading.get("temperatura_solo", reading.get("temperatura", 0))
    reading["ph"] = reading.get("ph", 0)
    return reading

@router.get("/leituras_solo/{agricultor_id}", response_model=List[LeituraSolo])
def obter_leituras_solo(agricultor_id: str):
    try:
        # Tenta converter para ObjectId (isso valida o formato do ID)
        try:
            agricultor_obj_id = ObjectId(agricultor_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="ID inválido")

        # Busca leituras diretamente pelo agricultor_id
        leituras = list(soil_collection.find({"agricultor_id": agricultor_obj_id}))
        return [serialize_soil_reading(l) for l in leituras]

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao obter leituras de solo: {str(e)}")
