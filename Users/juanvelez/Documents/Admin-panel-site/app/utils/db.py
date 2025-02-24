import json
import os
from datetime import datetime

class ScriptDB:
    def __init__(self):
        self.data_dir = os.path.join(os.getcwd(), "data")
        self.db_file = os.path.join(self.data_dir, "scripts.json")
        self._ensure_db()

    def _ensure_db(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.db_file):
            self._save_data({"scripts": {}, "metadata": {"lastUpdate": None, "totalScripts": 0}})

    def _save_data(self, data):
        with open(self.db_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_data(self):
        with open(self.db_file, "r") as f:
            return json.load(f)

    async def add_script(self, script_data):
        data = self._load_data()
        script_name = script_data["name"]
        data["scripts"][script_name] = {
            **script_data,
            "added": datetime.now().strftime("%Y-%m-%d"),
            "lastUpdated": datetime.now().strftime("%Y-%m-%d")
        }
        data["metadata"]["lastUpdate"] = datetime.now().isoformat()
        data["metadata"]["totalScripts"] = len(data["scripts"])
        self._save_data(data)
        return data["scripts"][script_name]

    async def get_all_scripts(self):
        data = self._load_data()
        return data["scripts"]