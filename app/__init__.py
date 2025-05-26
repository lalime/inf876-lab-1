from flask import Flask

def create_app():
    app = Flask(__name__)

    # 👇 Le bon import si imc_routes.py contient un Blueprint
    from app.routes.imc_routes import main_bp
    app.register_blueprint(main_bp)

    return app