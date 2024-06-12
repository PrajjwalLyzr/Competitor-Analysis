from flask import request, render_template, send_file
import tempfile
from reportlab.pdfgen import canvas
from src.Controllers import LyzrInitiallizer
import markdown
from src.utils import utils


def analysis():
    if request.method == 'POST':
        competitor_name = request.form.get('competitor_name')
        competitor_website = request.form.get('competitor_website')
        # metrics = request.form.get('key_metrics')

        LyzrInitiallizer.analyze_competitors(companyName=competitor_name, websiteName=competitor_website)
        LyzrInitiallizer.process_data(companyName=competitor_name, websiteName=competitor_website)
        strength, weakness, opportunity, threat = LyzrInitiallizer.swot_analysis(company_name=competitor_name, website_name=competitor_website)
        html_strength = markdown.markdown(strength)
        html_weakness = markdown.markdown(weakness)
        html_opportunity = markdown.markdown(opportunity)
        html_threats = markdown.markdown(threat) 
        with open(f'raw_data_files\{competitor_name}.txt', 'r') as file:
            text_data = file.read()  
        file_data = markdown.markdown(text_data) 
        return render_template('analysis.html', html_strength=html_strength, html_weakness=html_weakness, html_opportunity=html_opportunity, html_threats=html_threats, file_data=file_data)


def download_pdf():
    txt_file_path = utils.get_files_in_directory('raw_data_files')
    TEXT_FILE_PATH = txt_file_path[0]

    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        # Read the text file content
        with open(TEXT_FILE_PATH, "r") as text_file:
            text_content = text_file.read()

        # Generate the PDF using ReportLab
        # print(text_content)
        # Generate the PDF using ReportLab
        pdf = canvas.Canvas(pdf_file.name)

        # Current Y position for text placement (start from the bottom)
        y_pos = 800

        # Loop through each line in the text content
        for line in text_content.splitlines():
            # Write the line at the current Y position
            pdf.drawString(20, y_pos, line)

            # Adjust Y position for the next line (considering font size)
            y_pos -= 16  # Adjust based on your font size

        # Save the PDF document with entire content
        pdf.save()

    # Set headers for download
    return send_file(
        pdf_file.name,
        mimetype="application/pdf",
        as_attachment=True,
    )