from flask import Blueprint, jsonify, request

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')


@chat_bp.route('/', methods=['POST'])
def ask_gpt():
    """
    שליחת שאלה לבוט השקעות
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            message:
              type: string
              example: אני מחפש דירה להשקעה באזור המרכז
    responses:
      200:
        description: תשובה מהבוט
        examples:
          application/json: { "response": "נכסים מתאימים נמצאו..." }
    """
    user_message = request.json.get("message", "")
    return jsonify({"response": f"אתה אמרת: {user_message}"})
