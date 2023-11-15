from datetime import timedelta
from flask import Flask
from extensions import db, jwt
from auth import auth_bp
from main_routes import main_bp
from dotenv import load_dotenv

from models import populate_categories, populate_subcategories


#application factory function

load_dotenv()

def create_app():
    
    app = Flask(__name__)
 
    app.config.from_prefixed_env() # Load environment variables (only those that start with FLASK)


    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_CSRF_METHODS'] = ["POST", "PUT", "PATCH", "DELETE"]
    app.config['JWT_CSRF_IN_COOKIES'] = False
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'Access_token'
    app.config['JWT_REFRESH_COOKIE_NAME'] = 'Refresh_token'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 1800)))
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)

    # Initialize app
    db.init_app(app)

    with app.app_context():
        # Create the database and the tables
        db.create_all()
        populate_subcategories()
        populate_categories()
        

    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp) 
    app.register_blueprint(main_bp) 
    

    return app

