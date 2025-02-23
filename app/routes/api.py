from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
import os

router = APIRouter()

@router.get("/api/scripts/status")
async def get_scripts_status():
    try:
        script_path = os.path.join(os.getcwd(), "data", "scripts.json")
        with open(script_path, "r") as f:
            scripts_data = json.load(f)
            
        return {
            "status": "success",
            "total_scripts": len(scripts_data.get("scripts", {})),
            "last_update": datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
            "scripts": scripts_data.get("scripts", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/scripts/{script_name}")
async def get_script_info(script_name: str):
    try:
        script_path = os.path.join(os.getcwd(), "data", "scripts.json")
        with open(script_path, "r") as f:
            scripts_data = json.load(f)
            
        script = scripts_data.get("scripts", {}).get(script_name)
        if not script:
            raise HTTPException(status_code=404, detail="Script not found")
            
        return {
            "status": "success",
            "script": script
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))