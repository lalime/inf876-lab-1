from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
# from flask import session*
from pprint import pprint
import logging
from app.services.imc_service import ImcService
import app.services.database_handler as db_handler

logging.basicConfig(level=logging.DEBUG)

main_bp = Blueprint('main', __name__)
imc_service = ImcService()


@main_bp.route('/', methods=['GET', 'POST'])
def home():
    """
    Accueil et calcul IMC de l'utilisateur
    """
    imc = None
    if request.method == 'POST':
        poids = float(request.form['poids'])
        taille = float(request.form['taille'])
        imc = imc_service.calcul_imc(poids, taille)

        # Enregistrer l'IMC dans Firestore
        db_handler.save_imc(
            user_id=session.get('user_id', 'unknown'),
            imc_value=imc,
            mail=session.get('email', 'unknown'), 
            poids=poids,
            taille=taille
        )

    return render_template('imc-form.html', imc=imc)