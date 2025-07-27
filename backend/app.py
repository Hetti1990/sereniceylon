from flask import Flask
from flask_cors import CORS
from backend.models import db
from backend.photos import photos_bp
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_agency.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize extensions
db.init_app(app)

# Register Blueprints
app.register_blueprint(photos_bp, url_prefix='/api')

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
