from flask import Blueprint
from src.Controllers import GetController, PostController



CompetitorAnalysis = Blueprint('CompetitorAnalysis', __name__)

CompetitorAnalysis.route('/analysis', methods=['POST'])(PostController.analysis)
CompetitorAnalysis.route('/download_pdf', methods=['POST'])(PostController.download_pdf)