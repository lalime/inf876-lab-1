# base image Python
FROM python:3.10-slim

# dossier de travail
WORKDIR /app

# copier dépendances
COPY requirements.txt .

# installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# copier tout le projet
COPY . .

# exposer le port Flask
EXPOSE 5000

# commande pour lancer l'app
CMD ["flask", "--app", "main", "run", "--host=0.0.0.0", "--port=5000"]
