from flask import Blueprint, jsonify

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')


@chat_bp.route('/', methods=['GET'])
def get_chat():
    return jsonify({"message": "Chat route working!"})
