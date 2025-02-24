import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# No need for app.run() with FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)