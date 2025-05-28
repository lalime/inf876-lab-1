from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash("Veuillez vous connecter avant d'accéder au profil.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Mettre à jour les infos du profil
        pass
    return render_template('profile.html')

@profile_bp.route('/history')
def history():
    return render_template('history.html')
