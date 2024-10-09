from flask import Blueprint, request, jsonify
from models import User, Assignment
from flask_bcrypt import Bcrypt
from utils.validation import validate_registration, validate_login
from bson.objectid import ObjectId

admin_bp = Blueprint('admin_bp', __name__)
bcrypt = Bcrypt()

# Admin Registration
@admin_bp.route('/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    if not validate_registration(data):
        return jsonify({"message": "Invalid registration data"}), 400

    if User.find_by_email(data['email']):
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    data['password'] = hashed_password
    data['role'] = 'admin'
    User.create_user(data)
    return jsonify({"message": "Admin registered successfully"}), 201

# Admin Login
@admin_bp.route('/login', methods=['POST'])
def login_admin():
    data = request.get_json()
    if not validate_login(data):
        return jsonify({"message": "Invalid credentials"}), 400

    admin = User.find_by_email(data['email'])
    if admin and bcrypt.check_password_hash(admin['password'], data['password']):
        return jsonify({"message": "Admin login successful"}), 200
    return jsonify({"message": "Login failed"}), 401

# View Assignments
@admin_bp.route('/assignments', methods=['GET'])
def get_assignments():
    admin_name = request.args.get('admin')
    if not admin_name:
        return jsonify({"message": "Admin name is required"}), 400
    
    assignments = Assignment.find_by_admin(admin_name)
    return jsonify([{
        "id": str(assignment['_id']),
        "userId": assignment['userId'],
        "task": assignment['task'],
        "timestamp": assignment['timestamp']
    } for assignment in assignments]), 200

# Accept an Assignment
@admin_bp.route('/assignments/<assignment_id>/accept', methods=['POST'])
def accept_assignment(assignment_id):
    result = Assignment.update_assignment(ObjectId(assignment_id), 'accepted')
    if result.modified_count == 0:
        return jsonify({"message": "Assignment not found or already accepted"}), 404
    return jsonify({"message": "Assignment accepted"}), 200

# Reject an Assignment
@admin_bp.route('/assignments/<assignment_id>/reject', methods=['POST'])
def reject_assignment(assignment_id):
    result = Assignment.update_assignment(ObjectId(assignment_id), 'rejected')
    if result.modified_count == 0:
        return jsonify({"message": "Assignment not found or already rejected"}), 404
    return jsonify({"message": "Assignment rejected"}), 200
