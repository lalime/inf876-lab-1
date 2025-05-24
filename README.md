# Calculateur IMC - Flask & Firebase

## 📌 Description
Ce projet est une **application web** permettant aux utilisateurs de calculer leur **Indice de Masse Corporelle (IMC)** à partir de leur taille et poids. L'application est développée avec **Flask** et déployée sur **Firebase Hosting**.

## 🚀 Technologies utilisées
- **Python** (Framework Flask)
- **HTML/CSS** (Interface utilisateur)
- **JavaScript** (Validation côté client)
- **Firebase** (Déploiement et authentification)

## ⚙️ Installation
1. **Clonez le repo** :
   ```bash
   git clone https://github.com/votre-repo/imc-app.git
   cd imc-app
    ```


2. **Installez les dépendances :** :
   ```bash
    pip install -r requirements.txt
    ```


3. **Exécutez l'application localement :** 
   ```bash
    python main.py
    ```

4. **Accédez à l’application :**  Ouvrez http://127.0.0.1:5000 dans votre navigateur.

## 🔥 Déploiement sur Firebase

1. **Connectez-vous à Firebase :**

   ```bash
    firebase login
    ```

2. **Initialisez Firebase :**
   ```bash
    firebase init
    ```

3. **Déployez l’application :**
 
   ```bash
    firebase deploy
    ```

## 📖 Fonctionnalités
✔️ Saisie du poids et de la taille ✔️ Calcul automatique de l'IMC ✔️ Affichage du diagnostic IMC (Sous-poids, Normal, Surpoids, Obésité) ✔️ Déploiement facile avec Firebase

## 🛠️ Structure du projet

   ```bash
    imc-app/
    │── app/
    │   ├── static/         # Fichiers CSS & JS
    │   ├── templates/      # Pages HTML
    │   ├── main.py         # Code Flask
    │── requirements.txt    # Dépendances
    │── firebase.json       # Configuration Firebase
    │── README.md           # Document explicatif
```

## 🔗 Ressources utiles
- [Flask documentation](https://flask.palletsprojects.com/ "Flask documentation")
- [Firebase Hosting](https://firebase.google.com/docs/hosting "Firebase Hosting")


## 📌 Auteur
Ce projet est développé par A & L. N’hésitez pas à contribuer ! 😊