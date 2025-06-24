from flask import Blueprint, jsonify

agents_bp = Blueprint('agents', __name__, url_prefix='/agents')


@agents_bp.route('/', methods=['GET'])
def get_agents():
    return jsonify({"message": "Agents route working!"})
