import firebase_admin
from firebase_admin import auth, credentials
import logging
import pprint

def get_user_details(uid):    
    """
    Obtenir des informations de l'utilisateur
    Parameters:
    uid (string): UID de l'utilisateur à mettre à jour
    Returns:
    Json : {"name": name, "email": email} si utilisateur existe
    Json : {"error": "User not found"} si l'utilisateur n'existe pas
    """
    try:
        # Fetch the user by UID
        user = auth.get_user(uid)
        pretty_object = pprint.pformat(user)
        logging.debug(f"User ********* : {pretty_object}")
        
        # Extract name and email
        name = user.display_name
        email = user.email
        
        return {"name": name, "email": email}
    except auth.UserNotFoundError:
        return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}


def updated_user(uid, name):
    """
    Mise à jour des informations de l'utilisateur
    Parameters:
    uid (string): UID de l'utilisateur à mettre à jour
    name (string): Nouveau nom de l'utilisateur
    Returns:
    user (UserRecord): updated userRecord
    false : if exception occurs
    """
    if uid is None or name is None:
        return false

    try:
        user = auth.update_user(
            uid=uid,
            display_name= name
        )
        if user.uid:
            logging.debug(f"Successfully updated user: {user.uid}")
            return user
    except Exception as e:
        logging.error(f"Error updating user: {e}")
    
    return None