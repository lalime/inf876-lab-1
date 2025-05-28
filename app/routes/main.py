from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
# from flask import session*
from pprint import pprint
import logging

logging.basicConfig(level=logging.DEBUG)

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    imc = None
    if request.method == 'POST':
        poids = float(request.form['poids'])
        taille = float(request.form['taille'])
        imc = imc_service.calcul_imc(poids, taille)

        # Enregistrer l'IMC dans Firestore
        db_handler.save_imc(
            user_id=session.get('user_id', 'unknown'),
            imc_value=imc,
            mail=request.form.get('email', 'unknown'), 
            poids=poids,
            taille=taille
        )

    return render_template('imc-form.html', imc=imc)

""" # Ajoutez ici la vérification des identifiants
if email != "test@example.com" or password != "1234":
error = "Email ou mot de passe incorrect."
else:
session['user'] = email
return redirect(url_for('profile.profile'))
return render_template('login.html', error=error) """

""" if len(password) < 6:
            error = "Le mot de passe doit contenir au moins 6 caractères."
        else:
            flash("Inscription réussie ! Connectez-vous.", "success")
            return redirect(url_for('auth.login'))
    return render_template('register.html', error=error) """