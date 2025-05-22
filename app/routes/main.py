from flask import Blueprint, render_template, request
from app.services.imc_service import ImcService

main_bp = Blueprint('main', __name__)
imc_service = ImcService()

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    imc = None
    if request.method == 'POST':
        poids = float(request.form['poids'])
        taille = float(request.form['taille'])
        imc = imc_service.calcul_imc(poids, taille)
    return render_template('imc-form.html', imc=imc)
