from flask import Blueprint
from Controllers import GetController, PostController



CompetitorAnalysis = Blueprint('CompetitorAnalysis', __name__)

CompetitorAnalysis.route('/analysis', methods=['POST'])(PostController.analysis)