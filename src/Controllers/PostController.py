from flask import Flask, request, render_template
from Controllers import LyzrInitiallizer

def analysis():
    if request.method == 'POST':
        competitor_name = request.form.get('competitor_name')
        competitor_website = request.form.get('competitor_website')
        metrics = request.form.get('key_metrics')

        if metrics is None:
            # competitorData = LyzrInitiallizer.scrape_competitor_analysis(company_name=competitor_name, website_name=competitor_website)
            competitorData = f'This is Competitor Analysis of {competitor_name}, link:{competitor_website}'
            return render_template('analysis.html', competitorData=competitorData)

        else:
            competitorData = f'This is Competitor Analysis of {competitor_name}, link:{competitor_website}'
            return render_template('analysis.html', competitorData=competitorData)
            

