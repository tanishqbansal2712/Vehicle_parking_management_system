from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models.models import db, User
import os

# App Initialization
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'parking.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)
# HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')

# Flask-Login Setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.user import user_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

# Create DB Tables + Default Admin
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create default admin user 
        if not User.query.filter_by(username='admin').first():
            from werkzeug.security import generate_password_hash
            admin_user = User(
                username='admin',
                email='admin@parking.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()

    app.run(debug=True)
