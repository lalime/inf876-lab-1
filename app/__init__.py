from flask import Flask
import firebase_admin
from firebase_admin import credentials, auth, firestore
from app.routes import main_bp, auth_bp, profile_bp
from flask_session import Session
from datetime import timedelta
import logging
import logging.config
import os

# Load configuration from file
logging.config.fileConfig('logging_config.ini')


def create_app():
    """ 
    """
    app = Flask(__name__)
    # Load Firebase Admin SDK
    if not firebase_admin._apps:
        cred = credentials.Certificate("config.json")
        firebase_admin.initialize_app(cred)

    app.secret_key = "bzkdjboizehboizheobizebzeoihbzeohbzoebh"

    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set session lifetime
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Protect against XSS
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)

    

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(main_bp)

    return app