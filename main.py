from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
import json
import os
from datetime import datetime

app = FastAPI()

DATA_FILE = "downloads.json"

class DownloadData(BaseModel):
    name: str
    email: EmailStr
    whatsapp: str
    product: str

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: List[dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.post("/telechargement")
async def save_download(data: DownloadData):
    all_data = load_data()

    # Ajouter timestamp
    entry = data.dict()
    entry["timestamp"] = datetime.now().isoformat()

    all_data.append(entry)
    save_data(all_data)
    return {"message": "Enregistré avec succès", "data": entry}

@app.get("/telechargement")
async def get_all_downloads():
    return load_data()
