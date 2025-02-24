from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import scripts

app = FastAPI(title="Crystal Hub Admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scripts.router)

@app.get("/")
async def root():
    return {"status": "online", "service": "Crystal Hub Admin API"}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRIPTS_FILE = "data/scripts.json"

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/api/scripts")
async def get_scripts():
    try:
        with open(SCRIPTS_FILE, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scripts/update")
async def update_script(script_data: dict):
    try:
        with open(SCRIPTS_FILE, "r+") as f:
            data = json.load(f)
            
            script_name = script_data["name"]
            data["scripts"][script_name] = {
                "content": script_data["content"],
                "game": script_data["game"],
                "last_updated": datetime.now().isoformat(),
                "version": data["scripts"].get(script_name, {}).get("version", 0) + 1
            }
            
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            
        return {"status": "success", "message": f"Script {script_name} updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "online", "service": "Crystal Hub Admin API"}