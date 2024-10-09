from flask import Flask
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.config.from_object('config.Config')

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
