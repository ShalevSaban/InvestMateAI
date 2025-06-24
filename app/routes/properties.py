from flask import Blueprint, jsonify

properties_bp = Blueprint('properties', __name__, url_prefix='/properties')


@properties_bp.route('/', methods=['GET'])
def get_properties():
    return jsonify({"message": "Properties route working!"})
