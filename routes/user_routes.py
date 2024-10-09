from flask import Blueprint, request, jsonify
from models import User, Assignment
from flask_bcrypt import Bcrypt
from utils.validation import validate_registration, validate_login
from datetime import datetime

user_bp = Blueprint('user_bp', __name__)
bcrypt = Bcrypt()

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not validate_registration(data):
        return jsonify({"message": "Invalid data"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    data['password'] = hashed_password
    data['role'] = 'user'
    User.create_user(data)
    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not validate_login(data):
        return jsonify({"message": "Invalid credentials"}), 400

    user = User.find_by_email(data['email'])
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Login failed"}), 401

@user_bp.route('/upload', methods=['POST'])
def upload_assignment():
    data = request.get_json()
    data['timestamp'] = datetime.utcnow()
    Assignment.create_assignment(data)
    return jsonify({"message": "Assignment uploaded successfully"}), 201
