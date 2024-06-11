from flask import Flask, request, render_template
from Controllers import LyzrInitiallizer

def analysis():
    if request.method == 'POST':
        competitor_name = request.form.get('competitor_name')
        competitor_website = request.form.get('competitor_website')
        metrics = request.form.get('key_metrics')

        if metrics == "":
            # strength, weakness, opportunity = LyzrInitiallizer.swot_analysis(company_name=competitor_name, website_name=competitor_website)
            # aboutCompetitor = LyzrInitiallizer.search_competitor_analysis(company_name=competitor_name, website_name=competitor_website)
            # competitorData = LyzrInitiallizer.scrape_competitor_analysis(company_name=competitor_name, website_name=competitor_website)
            # competitorData = f'This is Competitor Analysis of {competitor_name}, link:{competitor_website}'
            # aboutCompetitor = 'This is competitor data'
            strength = """ 1. **Comprehensive Insights Platform**: Lyzr offers a wide range of insights across various functions, including sales, marketing, business development, product, customer service, and customer support, making it a one-stop-shop for growth operators. 2. **AI-Driven Recommendations**: Lyzr's AI-driven recommendations and deal insights help teams drive growth, increase sales efficiency, and make data-driven decisions. 3. **Flexible Pricing Strategy**: Lyzr provides a flexible and competitive pricing strategy, allowing it to adapt to changing market conditions and customer needs. """
            weakness = """ 1. **Holistic View**: Lyzr's comprehensive insights platform provides a 360-degree view of various business functions, enabling users to make informed decisions across multiple areas. 2. **AI-Driven Insights**: Lyzr's AI-driven recommendations and deal insights help users identify untapped potential, refine planning and strategy, and uncover key financial insights. 3. **Competitive Pricing**: Lyzr's flexible pricing strategy allows it to adapt to changing market conditions and customer needs, making it more competitive in the market.  """
            opportunity = """ 1. **Inventory Management:** ['lyzr'] may struggle with inventory management, which can lead to inefficiencies and increased costs. This can be due to inadequate inventory turnover, high inventory levels, or poor inventory tracking systems. 2. **Financial Performance:** ['lyzr'] may face challenges in generating cash from operations, which can impact its financial stability. This can be due to factors such as high receivables and inventory levels, or inefficient financial management practices. 3. **Operational Inefficiencies:** ['lyzr'] may have operational inefficiencies that hinder its performance. This can include issues with supply chain management, inefficient use of resources, or poor communication among departments. """
            threat = """ 1. **Custom GPTs and GPT Store**: The emergence of Custom GPTs (Generative Pre-trained Transformers) and the GPT Store offers Lyzr opportunities to develop tailored AI models for specific business needs, enhancing its competitive edge in the market. 2. **Large Language Models (LLMs)**: The increasing use of LLMs across diverse use cases, such as natural language processing, can be leveraged by Lyzr to develop specialized AI models for various domains and tasks. 3. **Enterprise AI Tooling Stack**: Understanding the Enterprise AI Tooling Stack is crucial for businesses aiming to harness the full potential of AI. Lyzr can focus on developing and integrating its AI stack to drive AI-driven innovation within organizations.  """
            return render_template('analysis.html', strength=strength, weakness=weakness, opportunity=opportunity, threat=threat)

        else:
            # strength,weakness, opportunity = LyzrInitiallizer.swot_analysis(company_name=competitor_name, website_name=competitor_website)
            # strength = swot[0]['task_output']
            # weakness = swot[1]['task_output']
            # opportunity = swot[2]['task_output']
            # threat = swot[3]['task_output']
            # pass
            return render_template('analysis.html', strength=strength, weakness=weakness, opportunity=opportunity, threat=threat)


