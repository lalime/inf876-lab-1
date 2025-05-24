class ImcService:
    def calcul_imc(self, poids, taille):
        return round(poids / (taille ** 2), 2)
