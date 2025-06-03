from flask import Blueprint, render_template, request, Flask, session, redirect, url_for
import firebase_admin
from firebase_admin import firestore
from firebase_admin import auth # Importez auth aussi pour l'authentification
from firebase_admin import credentials, auth, firestore
from flask_session import Session

from app.services.imc_service import ImcService
import app.services.database_handler as db_handler


db = firestore.client()


main_bp = Blueprint('main', __name__)

imc_service = ImcService()




# Route pour afficher le formulaire d'inscription (ou le rendre)
@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Email et mot de passe requis", 400 # Mauvaise requête

        try:
            # Crée un nouvel utilisateur dans Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password # ATTENTION: Envoyer le mot de passe en clair comme ça n'est pas recommandé pour un front-end public. Utilisez l'approche Jetons ID !
            )
            print(f'Utilisateur créé avec succès : {user.uid}')

            return "Inscription réussie ! Vous pouvez maintenant vous connecter."
        except Exception as e:
            print(f"Erreur d'inscription : {e}")
            # Gérer les erreurs (email déjà utilisé, mot de passe faible, etc.)
            return f"Erreur lors de l'inscription : {e}", 500 # Erreur serveur

    # Méthode GET: Afficher un formulaire d'inscription simple (HTML)
    return '''
        <form method="post">
            Email: <input type="email" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Sign Up">
        </form>
    '''

# Route pour afficher le formulaire de connexion et gérer la connexion
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_token = request.form.get('idToken')
        if not id_token:
            return "Jeton d'identité requis", 400

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            session['user_id'] = uid
            print(f'Utilisateur {uid} connecté avec succès')
            return redirect(url_for('profile.profile'))
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            return f"Erreur lors de la connexion : {e}", 401

    # Méthode GET: Afficher un formulaire de connexion simple (HTML)
    return redirect(url_for('main.calcul_imc'))

# Route pour la déconnexion
@main_bp.route('/logout')
def logout():
    # Supprime l'UID de la session Flask
    session.pop('user_id', None)
    return redirect(url_for('auth.login')) # Redirige vers la page de connexion

# Exemple de route qui nécessite l'authentification
@main_bp.route('/profile')
def profile():
    # Vérifie si l'UID est dans la session
    if 'user_id' in session:
        uid = session['user_id']
        return redirect(url_for('main.calcul_imc'))
    else:
        # Si l'UID n'est pas dans la session, l'utilisateur n'est pas connecté
        return redirect(url_for('auth.login')) # Redirige vers la page de connexion

# --- Routes pour l'IMC ---


@main_bp.route('/calcul_imc', methods=['GET', 'POST'])
def calcul_imc():
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


# Route pour afficher l'historique IMC (nécessite la connexion)
@main_bp.route('/historique_imc')
def historique_imc():
     if 'user_id' not in session:
        return redirect(url_for('auth.login'))

     uid = session['user_id']

     try:
         user_doc_ref = db.collection('users').document(uid)
         bmi_history_ref = user_doc_ref.collection('bmiHistory')

         # Récupérer les entrées d'historique, triées par date descendante
         history_entries = bmi_history_ref.order_by('date', direction=firestore.Query.DESCENDING).stream()

         history_list = []
         for entry in history_entries:
             entry_data = entry.to_dict()
             # Formater la date si nécessaire
             if 'date' in entry_data:
                 # Firestore timestamp to Python datetime
                 entry_data['date'] = entry_data['date'].strftime('%Y-%m-%d %H:%M:%S')
             history_list.append(entry_data)

         # Ici, vous passeriez history_list à votre template HTML Flask
         # Pour l'exemple simple, on affiche en texte brut ou simple HTML
         html_output = "<h2>Votre Historique IMC</h2>"
         if history_list:
             html_output += "<ul>"
             for entry in history_list:
                 html_output += f"<li>Date: {entry.get('date', 'N/A')}, IMC: {entry.get('bmiValue', 'N/A'):.2f}, Poids: {entry.get('weight', 'N/A')} kg, Taille: {entry.get('height', 'N/A')} m</li>"
             html_output += "</ul>"
         else:
             html_output += "<p>Aucun historique disponible.</p>"

         html_output += '<p><a href="/profile">Retour au profil</a></p>'
         html_output += '<p><a href="/logout">Déconnexion</a></p>'


         return html_output

     except Exception as e:
         print(f"Erreur lors de la récupération de l'historique : {e}")
         return "Erreur lors de la récupération de l'historique.", 500


# Redirection par défaut si pas de page spécifiée
@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile.profile'))
    else:
        return redirect(url_for('auth.login'))

