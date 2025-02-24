import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# No need for app.run() with FastAPI
from fastapi import FastAPI
from app.main import app as fastapi_app

app = fastapi_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("wsgi:app", host="0.0.0.0", port=8000, reload=True)