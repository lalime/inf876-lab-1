from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
import logging
from app.services.user import get_user_details, updated_user

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET', 'POST'])
def profile():
    logging.debug(f"Session in profile: {session}")
    if 'user_id' not in session:
        flash("Veuillez vous connecter avant d'accéder au profil.", "error")
        return redirect(url_for('auth.login'))

    user_data = get_user_details(session.get('user_id'))

    # En cas d'erreur rediriger vers la page d'accueil
    if 'error' in user_data:
        flash(user_data['error'], "error")
        return redirect(url_for('auth.login'))

    logging.debug(f"User data in profile : {user_data}")

    if request.method == 'POST':
        # Mettre à jour les infos du profil
        user_updated = updated_user(session.get('user_id'), request.form.get('display_name'))
        logging.debug(f"User updated : {user_updated}")
        
        if user_updated :
            flash("Profil mis à jour avec succès.", "success")
            user_data["name"] = user_updated.display_name
        else :
            flash("Erreur lors de la mise à jour du profil.", "error")

    return render_template('profile.html', user=user_data)

@profile_bp.route('/history')
def history():
    return render_template('history.html')
