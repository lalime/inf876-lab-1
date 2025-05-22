# import os
from flask import Flask, send_file, render_template, request
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    return app

def calcul_imc(poids, taille):
    return round(poids / (taille ** 2), 2)

# def main():
#    app.run(port=int(os.environ.get('PORT', 80)))
