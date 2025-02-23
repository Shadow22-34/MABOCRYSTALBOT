from fastapi import APIRouter
from ..utils.discord_webhook import send_script_update_alert

router = APIRouter()

@router.post("/scripts/update")
async def update_script(script_data: dict):
    try:
        script_name = script_data.get("name")
        script_version = script_data.get("version")
        await update_script_in_storage(script_data)
        await send_script_update_alert(
            script_name=script_name,
            action="Updated",
            version=script_version
        )
        return {"status": "success", "message": f"Script {script_name} updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/scripts/add")
async def add_script(script_data: dict):
    try:
        script_name = script_data.get("name")
        script_version = script_data.get("version")
        await add_script_to_storage(script_data)
        await send_script_update_alert(
            script_name=script_name,
            action="Added",
            version=script_version
        )
        return {"status": "success", "message": f"Script {script_name} added successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}