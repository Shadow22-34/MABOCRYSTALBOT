import json
import os
from datetime import datetime

class ScriptManager:
    def __init__(self):
        self.scripts_file = "data/scripts.json"
        self.ensure_data_dir()

    def ensure_data_dir(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.scripts_file):
            with open(self.scripts_file, "w") as f:
                json.dump({"scripts": {}, "last_updated": None}, f, indent=4)

    def save_script(self, name, content, game=""):
        with open(self.scripts_file, "r+") as f:
            data = json.load(f)
            data["scripts"][name] = {
                "content": content,
                "game": game,
                "last_updated": datetime.now().isoformat(),
                "version": data["scripts"].get(name, {}).get("version", 0) + 1
            }
            data["last_updated"] = datetime.now().isoformat()
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        return True

    def get_version(self, name):
        with open(self.scripts_file, "r") as f:
            data = json.load(f)
            return data["scripts"].get(name, {}).get("version", 0)