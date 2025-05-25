from flask import Flask, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, auth, firestore
# from werkzeug.security import generate_password_hash, check_password_hash # Potentiellement utile mais pas avec l'approche direct-auth

# ... (Initialisation Firebase Admin SDK comme vu précédemment) ...

app = Flask(__name__)
app.secret_key = 'une_cle_secrete_tres_securisee_a_changer_!' # Indispensable pour les sessions Flask !

# Assurez-vous que l'app Firebase est initialisée (copiez/collez le bloc d'initialisation ici si vous ne l'avez pas déjà en dehors des routes)
# cred = credentials.Certificate('chemin/vers/votre/cle-service.json')
# if not firebase_admin._apps:
#     firebase_admin.initialize_app(cred)
# db = firestore.client()


# Route pour afficher le formulaire d'inscription (ou le rendre)
@app.route('/signup', methods=['GET', 'POST'])
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Email et mot de passe requis", 400

        try:
            # ATTENTION: Le Admin SDK NE PERMET PAS de vérifier directement un mot de passe.
            # Cette approche est INCORRECTE pour vérifier des identifiants client avec l'Admin SDK.
            # Pour une connexion, le flow sécurisé implique que le client utilise le SDK client pour se connecter
            # et envoie le jeton ID généré au backend pour vérification.

            # Voici comment on VÉRIFIE un JETON ID ENVOYÉ PAR LE CLIENT
            # Si votre front-end utilise le SDK client Firebase pour se connecter (email/password),
            # il obtiendra un 'ID token'. Ce jeton doit être envoyé à cette route POST.
            id_token = request.form.get('idToken') # Exemple: le client envoie le jeton dans un champ de formulaire

            if not id_token:
                 return "Jeton d'identité requis", 400

            # Vérifie le jeton ID - C'est LA BONNE MÉTHODE avec l'Admin SDK pour l'authentification client
            # Cette fonction vérifie la signature du jeton et s'assure qu'il est valide et non expiré.
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']

            # L'utilisateur est authentifié avec succès !
            # Stockez l'UID dans la session Flask
            session['user_id'] = uid

            print(f'Utilisateur {uid} connecté avec succès')
            return redirect(url_for('profile')) # Redirige vers une page profil ou tableau de bord

        except Exception as e:
            print(f"Erreur de connexion : {e}")
            # Gérer les erreurs (mauvais mot de passe, utilisateur inexistant, jeton invalide/expiré, etc.)
            return f"Erreur lors de la connexion : {e}", 401 # Non autorisé

    # Méthode GET: Afficher un formulaire de connexion simple (HTML)
    return '''
        <form method="post">
            Email: <input type="email" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
        <p>Pas encore de compte? <a href="/signup">Inscrivez-vous ici</a>.</p>
    '''

# Route pour la déconnexion
@app.route('/logout')
def logout():
    # Supprime l'UID de la session Flask
    session.pop('user_id', None)
    return redirect(url_for('login')) # Redirige vers la page de connexion

# Exemple de route qui nécessite l'authentification
@app.route('/profile')
def profile():
    # Vérifie si l'UID est dans la session
    if 'user_id' in session:
        uid = session['user_id']
        # Vous pouvez optionnellement charger les données de l'utilisateur depuis Firestore ici
        # user_doc = db.collection('users').document(uid).get()
        # user_data = user_doc.to_dict() if user_doc.exists else {}
        # return f"Bienvenue, utilisateur {uid}! Voici votre profil." # ou render_template avec user_data
        return f"Bienvenue, utilisateur {uid}! Vous êtes connecté."
    else:
        # Si l'UID n'est pas dans la session, l'utilisateur n'est pas connecté
        return redirect(url_for('login')) # Redirige vers la page de connexion

# --- Routes pour l'IMC ---
# Vous modifierez votre route de calcul IMC pour qu'elle nécessite la connexion
@app.route('/calcul_imc', methods=['GET', 'POST'])
def calcul_imc():
    if 'user_id' not in session:
        return redirect(url_for('login')) # L'utilisateur doit être connecté pour calculer

    uid = session['user_id'] # Récupère l'UID de l'utilisateur connecté

    if request.method == 'POST':
        # ... (Votre logique de calcul IMC actuelle) ...
        poids = float(request.form.get('poids'))
        taille = float(request.form.get('taille'))
        # Calcul IMC ...

        imc_resultat = poids / (taille * taille) # Exemple simple

        # Maintenant, stockez ce résultat dans Firestore pour l'utilisateur connecté
        try:
            user_doc_ref = db.collection('users').document(uid)
            bmi_history_ref = user_doc_ref.collection('bmiHistory')
            bmi_data = {
                'weight': poids,
                'height': taille,
                'bmiValue': imc_resultat,
                'date': firestore.SERVER_TIMESTAMP # Utilisez le timestamp du serveur Firebase
            }
            bmi_history_ref.add(bmi_data)
            print(f"IMC enregistré pour l'utilisateur {uid}")

            return f"Votre IMC calculé est : {imc_resultat}. Il a été enregistré." # Ou rediriger vers l'historique
        except Exception as e:
            print(f"Erreur lors de l'enregistrement IMC : {e}")
            return "Erreur lors de l'enregistrement de l'IMC.", 500

    # Méthode GET: Afficher un formulaire de calcul IMC simple (HTML)
    return '''
        <h2>Calculer votre IMC</h2>
        <form method="post">
            Poids (kg): <input type="text" name="poids"><br>
            Taille (m): <input type="text" name="taille"><br>
            <input type="submit" value="Calculer et Enregistrer">
        </form>
        <p><a href="/profile">Retour au profil</a></p>
        <p><a href="/logout">Déconnexion</a></p>
    '''


# Route pour afficher l'historique IMC (nécessite la connexion)
@app.route('/historique_imc')
def historique_imc():
     if 'user_id' not in session:
        return redirect(url_for('login'))

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
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    # N'oubliez pas de définir FLASK_ENV=development et FLASK_APP=votre_fichier.py
    # et de lancer avec 'flask run' pour le développement.
    # Utilisez un serveur WSGI pour la production.
    app.run(debug=True)
