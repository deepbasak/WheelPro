import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-for-premium-rims-2025")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize Cloudinary if environment variables are set
if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    from cloud_storage import initialize_cloudinary
    initialize_cloudinary()
    app.config['USE_CLOUDINARY'] = True
else:
    app.config['USE_CLOUDINARY'] = False
    logging.warning("Cloudinary environment variables not set. File uploads will use local storage.")

# Configure database
database_url = os.environ.get("DATABASE_URL")
# Heroku uses 'postgres://' but SQLAlchemy 1.4+ requires 'postgresql://'
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure WTF settings
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = None

# Initialize the database
db.init_app(app)

# Import models and routes after app creation
from models import *
from routes import *

with app.app_context():
    db.create_all()
    # Initialize sample data if no products exist
    from data_store import initialize_sample_data
    initialize_sample_data()

if __name__ == '__main__':
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
