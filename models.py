from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')
mongo = PyMongo(app)

class User:
    @staticmethod
    def create_user(data):
        user_data = {
            "username": data['username'],
            "email": data['email'],
            "password": data['password'],
            "role": data['role'],
        }
        return mongo.db.users.insert_one(user_data)

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

class Assignment:
    @staticmethod
    def create_assignment(data):
        assignment_data = {
            "userId": data['userId'],
            "task": data['task'],
            "admin": data['admin'],
            "status": "pending",
            "timestamp": data.get('timestamp')
        }
        return mongo.db.assignments.insert_one(assignment_data)

    @staticmethod
    def find_by_admin(admin_name):
        return mongo.db.assignments.find({"admin": admin_name})

    @staticmethod
    def update_assignment(assignment_id, status):
        return mongo.db.assignments.update_one(
            {"_id": assignment_id},
            {"$set": {"status": status}}
        )
