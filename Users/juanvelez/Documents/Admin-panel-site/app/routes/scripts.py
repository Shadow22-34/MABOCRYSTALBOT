from flask import Blueprint, request, jsonify
from ..utils.script_manager import ScriptManager
from ..utils.discord_notifier import DiscordNotifier
import os

scripts = Blueprint('scripts', __name__)
script_manager = ScriptManager()
notifier = DiscordNotifier(os.getenv('DISCORD_WEBHOOK_URL'))

@scripts.route('/api/scripts/save', methods=['POST'])
async def save_script():
    data = request.json
    script_name = data.get('name')
    content = data.get('content')
    game = data.get('game', '')

    try:
        script_manager.save_script(script_name, content, game)
        await notifier.notify_script_update(script_name, script_manager.get_version(script_name))
        return jsonify({"status": "success", "message": "Script saved successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500