import json
import os
from datetime import datetime

print("🔍 Starting script manager...")

# Initialize storage
SCRIPTS_FILE = "scripts.json"

# Create scripts.json if it doesn't exist
if not os.path.exists(SCRIPTS_FILE):
    print("📝 Creating new scripts database...")
    with open(SCRIPTS_FILE, "w") as f:
        json.dump({"scripts": {}, "last_updated": None}, f, indent=4)
    print("✅ Database created")

# Test script
test_script = """
local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer

print("Test Basketball Script")
"""

try:
    # Read current data
    with open(SCRIPTS_FILE, "r") as f:
        data = json.load(f)
        print("📖 Loaded existing scripts")

    # Add new script
    data["scripts"]["basketball_legends"] = {
        "content": test_script,
        "game": "Basketball Legends",
        "last_updated": datetime.now().isoformat(),
        "version": data["scripts"].get("basketball_legends", {}).get("version", 0) + 1
    }
    
    # Save updated data
    with open(SCRIPTS_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("💾 Saved script successfully")

    # Verify saved data
    print("\n📊 Current scripts in storage:")
    for name, script in data["scripts"].items():
        print(f"\n🎮 {name}:")
        print(f"  Version: {script['version']}")
        print(f"  Updated: {script['last_updated']}")
        print(f"  Content Length: {len(script['content'])} characters")

except Exception as e:
    print(f"❌ Error: {str(e)}")