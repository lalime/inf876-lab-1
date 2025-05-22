class ImcService:
    def calcul_imc(poids, taille):
        return round(poids / (taille ** 2), 2)
