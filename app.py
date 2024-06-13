from flask import Flask, request, render_template, send_file
import pandas as pd
from fpdf import FPDF
from openpyxl import Workbook
import io
from routes import CompetitorAnalysis

app = Flask(__name__)
app.register_blueprint(CompetitorAnalysis, url_prefix='')


@app.route('/')
def index():
    return render_template('index.html')




# if __name__ == "__main__":
#     app.run(debug=True)

