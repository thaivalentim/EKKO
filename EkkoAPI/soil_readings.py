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
db = client["EkkoDB_UnifiedUser"]
soil_collection = db["leituras_solo"]

router = APIRouter()

class LeituraSolo(BaseModel):
    data_leitura: str
    ph: float = Field(0, ge=0)
    umidade: float = Field(..., ge=0)
    temperatura: float = Field(...)
    dispositivo: str = ""
    condutividade_eletrica: float = 0
    salinidade: float = 0
    NPK: float = 0

from datetime import datetime

def serialize_soil_reading(reading) -> dict:
    reading["_id"] = str(reading["_id"])
    # Use 'usuario_id' as per your database structure
    if "usuario_id" in reading:
        reading["usuario_id"] = str(reading["usuario_id"])
    else:
        reading["usuario_id"] = ""

    # Handle timestamp conversion safely
    timestamp = reading.get("timestamp") or reading.get("data_leitura")
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
    reading["dispositivo"] = reading.get("dispositivo", "")
    reading["umidade"] = reading.get("umidade_solo", reading.get("umidade", 0))
    reading["temperatura"] = reading.get("temperatura_solo", reading.get("temperatura", 0))
    reading["ph"] = reading.get("pH", reading.get("ph", 0))
    reading["condutividade_eletrica"] = reading.get("condutividade_eletrica", 0)
    reading["salinidade"] = reading.get("salinidade", 0)
    reading["NPK"] = reading.get("NPK", 0)
    return reading

@router.get("/leituras_solo/{usuario_id}", response_model=List[LeituraSolo])
def obter_leituras_solo(usuario_id: str):
    try:
        # Tenta converter para ObjectId (isso valida o formato do ID)
        try:
            usuario_obj_id = ObjectId(usuario_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="ID inválido")

        # Busca leituras diretamente pelo usuario_id
        leituras = list(soil_collection.find({"usuario_id": usuario_obj_id}))
        return [serialize_soil_reading(l) for l in leituras]

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao obter leituras de solo: {str(e)}")

@router.get("/leituras_solo", response_model=List[LeituraSolo])
def obter_todas_leituras_solo():
    try:
        leituras = list(soil_collection.find())
        return [serialize_soil_reading(l) for l in leituras]
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao obter todas leituras de solo: {str(e)}")
