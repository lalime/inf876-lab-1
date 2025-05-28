from flask import Flask
import firebase_admin
from firebase_admin import credentials, auth, firestore
from app.routes import main_bp, auth_bp, profile_bp

def create_app():
    app = Flask(__name__)
    cred = credentials.Certificate('imcalcultor-firebase-adminsdk-fbsvc-0629222380.json')
    firebase_admin.initialize_app(cred)

    app.secret_key = "bzkdjboizehboizheobizebzeoihbzeohbzoebh"
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(main_bp)

    return app