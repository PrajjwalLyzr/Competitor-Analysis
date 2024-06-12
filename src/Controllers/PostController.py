from flask import request, render_template
from Controllers import LyzrInitiallizer
import markdown

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

       