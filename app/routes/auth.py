from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import firestore, auth, credentials
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Formulaire de connexion utilisateur
    """
    error = None
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        id_token = request.form.get('idToken')
        f_error = request.form.get('error')

        if not id_token:
            error = f"Echec de connexion : Login ou mot de passe incorrect"
        else :
            try:
                decoded_token = auth.verify_id_token(id_token)

                uid = decoded_token['uid']
                session['user_id'] = uid
                flash(f'Utilisateur {uid} connecté avec succès', "success")

                return redirect(url_for('profile.profile'))
            except Exception as e:
                error = f"Echec de connexion : {e}"
                # print(f"Echec de connexion : {e}")
        
    return render_template('login.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Formulaire de création de profil utilisateur
    """
    error = None
    if request.method == 'POST':
        name = request.form['display_name']
        email = request.form['email']
        password = request.form['password']
        # Ajoutez ici l'enregistrement en base de données

        if not email or not password:
            error = "Email et mot de passe requis", 400 # Mauvaise requête

        try:
            # Crée un nouvel utilisateur dans Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password # ATTENTION: Envoyer le mot de passe en clair comme ça n'est pas recommandé pour un front-end public. Utilisez l'approche Jetons ID !
            )
            error = f'Utilisateur créé avec succès : {user.uid}'

            flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "success")
            return redirect(url_for('profile.profile'))
        except Exception as e:
            print(f"Erreur d'inscription : {e}")
            # Gérer les erreurs (email déjà utilisé, mot de passe faible, etc.)
            error = f"Erreur lors de l'inscription : {e}" # Erreur serveur

    return render_template('register.html', error=error)


# Route pour la déconnexion
@auth_bp.route('/logout')
def logout():
    """
    Deconnexion et suppression de la session de l'utilisateur
    """
    # Supprime l'UID de la session Flask
    session.pop('user_id', None)
    return redirect(url_for('auth.login')) # Redirige vers la page de connexion
