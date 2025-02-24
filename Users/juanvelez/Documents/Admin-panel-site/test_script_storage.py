import asyncio
from app.utils.script_manager import ScriptManager
from app.utils.discord_notifier import DiscordNotifier

import asyncio
import json
import os
import sys
from datetime import datetime

def test_basketball_legends():
    print("\n🔄 Testing Basketball Legends script storage...")
    
    test_script = """
    local Players = game:GetService("Players")
    local LocalPlayer = Players.LocalPlayer
    
    print("Test Basketball Script")
    """
    
    manager = ScriptManager()
    try:
        result = manager.save_script(
            name="basketball_legends",
            content=test_script,
            game="Basketball Legends"
        )
        print("\n📊 Verifying saved data...")
        
        with open(manager.scripts_file, "r") as f:
            data = json.load(f)
            print("\n📁 Current scripts in storage:", data)
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    print("🔍 Current working directory:", os.getcwd())
    test_basketball_legends()