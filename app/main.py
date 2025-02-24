from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import os

# Create the FastAPI app instance
app = FastAPI(title="Crystal Hub Admin API")

# Configure webhook
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
webhook_notifier = discord_webhook.DiscordNotifier(WEBHOOK_URL)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with webhook dependency
app.include_router(api.router)
app.include_router(
    scripts.router,
    dependencies=[{"webhook": webhook_notifier}]
)

# Initialize data directory
data_dir = os.path.join(os.getcwd(), "data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    with open(os.path.join(data_dir, "scripts.json"), "w") as f:
        json.dump({"scripts": {}, "metadata": {"lastUpdate": None, "totalScripts": 0}}, f)

@app.get("/")
async def root():
    return {"status": "online", "service": "Crystal Hub Admin API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Make sure app is explicitly exported
__all__ = ['app']