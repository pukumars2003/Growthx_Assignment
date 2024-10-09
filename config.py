import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '4a57fc810e379706d704a1e4022a4a04964182443013b272')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/assignment_portal')
