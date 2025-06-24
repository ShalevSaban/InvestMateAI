from flask import Blueprint, jsonify

agents_bp = Blueprint('agents', __name__, url_prefix='/agents')


@agents_bp.route('/', methods=['GET'])
def get_agents():
    """
    קבלת רשימת סוכנים
    ---
    responses:
      200:
        description: הצלחה
        examples:
          application/json: { "message": "Agents route working!" }
    """
    return jsonify({"message": "Agents route working!"})
