from flask import Blueprint, render_template, request, Flask, session, redirect, url_for
import firebase_admin
from firebase_admin import firestore
from firebase_admin import auth # Importez auth aussi pour l'authentification
from firebase_admin import credentials, auth, firestore
from flask_session import Session

# from werkzeug.security import generate_password_hash, check_password_hash # Potentiellement utile mais pas avec l'approche direct-auth

# ... (Initialisation Firebase Admin SDK comme vu précédemment) ...

# Remplacez 'chemin/vers/votre/cle-service.json' par le chemin réel de votre fichier
cred = credentials.Certificate('imcalcultor-firebase-adminsdk-fbsvc-0629222380.json')
firebase_admin.initialize_app(cred)

# Obtenez une référence vers la base de données Firestore
db = firestore.client()

# Vous pouvez maintenant utiliser 'db' pour interagir avec Firestore
# et 'auth' (via firebase_admin.auth) pour gérer les utilisateurs Auth
app = Flask(__name__)
app.secret_key = "bzkdjboizehboizheobizebzeoihbzeohbzoebh"
main_bp = Blueprint('main', __name__)

# ...toutes tes routes @main_bp.route...

# Enregistre le blueprint sur l'app Flask




# Assurez-vous que l'app Firebase est initialisée (copiez/collez le bloc d'initialisation ici si vous ne l'avez pas déjà en dehors des routes)
# cred = credentials.Certificate('chemin/vers/votre/cle-service.json')
# if not firebase_admin._apps:
#     firebase_admin.initialize_app(cred)
# db = firestore.client()


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

            # Optionnel: Stocker des infos supplémentaires dans Firestore lors de l'inscription
            # db.collection('users').document(user.uid).set({
            #    'email': email,
            #    'createdAt': firestore.SERVER_TIMESTAMP
            # })

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
            return redirect(url_for('main.profile'))
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
    return redirect(url_for('main.login')) # Redirige vers la page de connexion

# Exemple de route qui nécessite l'authentification
@main_bp.route('/profile')
def profile():
    # Vérifie si l'UID est dans la session
    if 'user_id' in session:
        uid = session['user_id']
        return redirect(url_for('main.calcul_imc'))
    else:
        # Si l'UID n'est pas dans la session, l'utilisateur n'est pas connecté
        return redirect(url_for('main.login')) # Redirige vers la page de connexion

# --- Routes pour l'IMC ---


@main_bp.route('/calcul_imc', methods=['GET', 'POST'])
def calcul_imc():
    imc = None
    if request.method == 'POST':
        poids = float(request.form['poids'])
        taille = float(request.form['taille'])
        # imc = imc_service.calcul_imc(poids, taille)
        imc = round(poids / (taille ** 2), 2)
    return render_template('imc-form.html', imc=imc)


# Route pour afficher l'historique IMC (nécessite la connexion)
@main_bp.route('/historique_imc')
def historique_imc():
     if 'user_id' not in session:
        return redirect(url_for('main.login'))

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
        return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('main.login'))

app.register_blueprint(main_bp)


if __name__ == "__main__":
    app.debug = True
    app.run()