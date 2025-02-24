from flask import Blueprint, jsonify
from ..utils.script_manager import ScriptManager

api = Blueprint('api', __name__)
script_manager = ScriptManager()

@api.route('/api/scripts/list', methods=['GET'])
def list_scripts():
    return jsonify(script_manager.get_all_scripts())

@api.route('/api/scripts/get/<name>', methods=['GET'])
def get_script(name):
    script = script_manager.get_script(name)
    if script:
        return jsonify(script)
    return jsonify({"error": "Script not found"}), 404