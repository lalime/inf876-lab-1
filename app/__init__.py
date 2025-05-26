from flask import Flask
import firebase_admin
from firebase_admin import credentials, auth, firestore

def create_app():
    app = Flask(__name__)
    cred = credentials.Certificate('imcalcultor-firebase-adminsdk-fbsvc-0629222380.json')
    firebase_admin.initialize_app(cred)

    app.secret_key = "bzkdjboizehboizheobizebzeoihbzeohbzoebh"
    from app.routes.imc_routes import main_bp
    app.register_blueprint(main_bp)

    return app