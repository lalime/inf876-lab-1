import firebase_admin
from firebase_admin import credentials, firestore
import logging

if not firebase_admin._apps:
    cred = credentials.Certificate("config.json")
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def save_imc(user_id, imc_value, mail, poids, taille, date=None):
    """
    Sauvegarde les données de l'IMC dans Firestore.
    """
    data = {
        "user_id": user_id,
        "user_email": mail,
        "poids": poids,
        "taille": taille,  # Assuming taille is the same as imc_value for simplicity
        "imc": imc_value,
        "date": date or firestore.SERVER_TIMESTAMP,
    }
    print(f"Saving IMC data: {data}")
    return db.collection("imc_calculs").add(data)

def get_user_imc(user_id):
    """
    Récupère l'historique IMC d'un utilisateur spécifique.
    """
    imcs = db.collection("imc_calculs").where("user_id", "==", user_id).stream()
    
    return [doc.to_dict() for doc in imcs]