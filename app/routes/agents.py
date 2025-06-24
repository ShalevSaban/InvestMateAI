from flask import Blueprint, request, jsonify
from flasgger import swag_from
from werkzeug.security import generate_password_hash
from app.models.agent import Agent
from app import db

agents_bp = Blueprint('agents', __name__)


@agents_bp.route('/agents/', methods=['POST'])
@swag_from({
    'tags': ['Agents'],
    'description': 'Create a new agent',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'full_name': {'type': 'string'},
                    'phone_number': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['full_name', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'Agent created successfully'},
        400: {'description': 'Email already exists or invalid input'}
    }
})
def create_agent():
    data = request.get_json()

    if not data or not all(k in data for k in ['full_name', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400

    if Agent.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    hashed_password = generate_password_hash(data['password'])

    agent = Agent(
        full_name=data['full_name'],
        phone_number=data.get('phone_number'),
        email=data['email'],
        password_hash=hashed_password
    )

    db.session.add(agent)
    db.session.commit()

    return jsonify({'message': 'Agent created successfully'}), 201
