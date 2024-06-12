import ast
import datetime
import os
import re
import json
from src.utils import utils
import newspaper
from dotenv import load_dotenv
from gnews import GNews
from lyzr_automata import Agent, Task
from lyzr_automata.ai_models.openai import OpenAIModel
# from lyzr_automata.memory.open_ai import OpenAIMemory
from lyzr_automata.ai_models.perplexity import PerplexityModel
from lyzr_automata.tasks.task_literals import InputType, OutputType

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

FOLDER_NAME = "raw_data_files"
AGENTS_FILE = "assistant_ids.json"
REPORT_FOLDER_NAME = "reports"


# FUNCTIONS

open_ai_model_text = OpenAIModel(
    api_key=OPENAI_API_KEY,
    parameters={
        "model": "gpt-4o",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

perplexity_model_text = PerplexityModel(
    api_key=PERPLEXITY_API_KEY,
    parameters={
        "model": "llama-3-sonar-small-32k-online",
    },
)



def search_competitor_analysis(company_name, website_name):
    search_task = Task(
        name="Website data search",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=perplexity_model_text,
        instructions=f"Tell me about the company {company_name} - {website_name}",
        log_output=True,
    ).execute()

    return search_task["choices"][0]["message"]["content"]


def scrape_competitor_analysis(company_name, website_name):
    scraped_data = ""
    google_news = GNews(period="7d", max_results=25)
    company_news = google_news.get_news(company_name)
    website_name = utils.remove_www(website_name)
    website_news = google_news.get_news_by_site(website_name)

    news_article_list = []
    news_dict = {}
    for news in company_news:
        news_article_list.append(news["title"])
        key = utils.format_key(news["title"])
        news_dict[key] = news

    for news in website_news:
        news_article_list.append(news["title"])
        key = utils.format_key(news["title"])
        news_dict[key] = news

    news_picker_agent = Agent(
        prompt_persona=f"""You are an expert news analyst. You have been given a list of news article headlines about a company. Your task is to identify and return the top 10 headlines that are the most important and impactful.
Consider the following criteria when evaluating each headline:
- Uniqueness: Avoid selecting multiple headlines that discuss the same event or topic. Each of the top 10 headlines should cover a distinct and different event or aspect.
- Relevance: How directly the headline pertains to significant events or developments related to the company (e.g., major financial moves, significant product launches, legal issues, executive changes, etc.).
- Impact: The potential effect of the news on the company's operations, stock price, public perception, or industry standing.

OUTPUT FORMAT - A list containing the headlines - [Headline 1, Headline 2, ...] - Output the list of articles in a Python-friendly format, with each item in the list properly enclosed in quotes and the entire list enclosed in square brackets.Do not include any additional tags or language indicators.

Please return the top 10 headlines. If the input has less than 10 headlines, return all. Make sure all the headlines are returned in the same format as input.
""",
        role="News picker",
    )

    news_picker_task = Task(
        name="Filter News Task",
        agent=news_picker_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Filter the news results and give top 10 headlines in a list. Return ONLY the list",
        log_output=True,
        enhance_prompt=False,
        default_input=news_article_list,
    ).execute()

    if news_picker_task:
        headlines_list = ast.literal_eval(news_picker_task)
        cleaned_headlines = [utils.format_key(headline.strip()) for headline in headlines_list]

        for title in cleaned_headlines:
            url = news_dict[title]["url"]
            date = news_dict[title]["published date"]
            try:
                full_article = google_news.get_full_article(url)
                article_title = full_article.title
                article_text = full_article.text
                scraped_data += (
                    "Title: "
                    + article_title
                    + "\nPublished Date: "
                    + date
                    + "\n"
                    + article_text
                    + "\n"
                )
            except:
                print("Error")

    return scraped_data


def specific_research_analysis(company_name, website_name, specific_research_area):
    search_task = Task(
        name="Specific data search",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=perplexity_model_text,
        instructions=f"Find detailed information about {specific_research_area} of the company {company_name} - {website_name}",
        log_output=True,
    ).execute()

    return search_task["choices"][0]["message"]["content"]

def swot_analysis(company_name, website_name=None):
    Analyst = Agent(
        prompt_persona=f"""
                        You are an analyst who is expert in SWOT analysis and your task is to conducting a comprehensive SWOT analysis for a company named [{company_name}] and its website [{website_name}] your analysis should consider various internal and external factors. 
                        The SWOT analysis will help the company understand its current strategic position and identify areas for improvement and growth.
                        """,
        role="Analyst"
    )

    Strength = Task(
        name="Finding Strenght of Company",
        agent=Analyst,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=perplexity_model_text,
        instructions=f"What are the key strengths of company:[{company_name}]? Please provide one heading and exactly three bullet points highlighting our major strengths.",
        log_output=True,
    ).execute()

    Weakness = Task(
        name="Finding Weakness of Company",
        agent=Analyst,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=perplexity_model_text,
        instructions=f"What are the primary weaknesses of company:[{company_name}]? Please provide one heading and exactly three bullet points detailing our main weaknesses.",
        log_output=True,
    ).execute()

    Opportunities = Task(
        name="Finding Opportunities of Company",
        agent=Analyst,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=perplexity_model_text,
        instructions=f"What are the opportunities available to company:[{company_name}] in the market? Please provide one heading and exactly three bullet points describing the main opportunities we can capitalize on.",
        log_output=True,
    ).execute()

    Threats = Task(
        name="Finding Threats of Company",
        agent=Analyst,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=perplexity_model_text,
        instructions=f"What are the significant threats facing company[{company_name}]? Please provide one heading and exactly three bullet points outlining the main threats we need to be aware of.",
        log_output=True,
    ).execute()
    

    return Strength["choices"][0]["message"]["content"], Weakness["choices"][0]["message"]["content"], Opportunities["choices"][0]["message"]["content"], Threats["choices"][0]["message"]["content"]


def save_raw_data_file(
    competitor_name, search_results="", scrape_results="", specific_research_results=""
):
    specific_research_raw_data = ""
    if specific_research_results:
        specific_research_raw_data = (
            f"Specific Research:\n{specific_research_results}\n"
        )
    raw_data = (
        f"{specific_research_raw_data}General Research:\n{search_results}\nRecent Articles about {competitor_name}:\n"
        + scrape_results
    )
    FILE_NAME = os.path.join(FOLDER_NAME, competitor_name + ".txt")
    # sentences = re.split(r"\.(?=\s)", raw_data)
    with open(FILE_NAME, "w") as my_file:
        # for sentence in sentences:
        #     my_file.write(sentence + "\n")
        my_file.write(raw_data)


def analyze_competitors(companyName, websiteName, specific_research_area=""):
    utils.create_folder(folder_name=FOLDER_NAME, report_folder_name=REPORT_FOLDER_NAME, agent_file=AGENTS_FILE)

    specific_research_results = ""
    if specific_research_area != "":
        specific_research_results = specific_research_analysis(
            company_name=companyName, website_name=websiteName, specific_research_area=specific_research_area
        )
    search_results = search_competitor_analysis(
        company_name=companyName, website_name=websiteName
    )
    # scrape_results = scrape_competitor_analysis(
    #     company_name=companyName, website_name=websiteName
    # )
    
    # save_raw_data_file(
    #     companyName,
    #     search_results,
    #     scrape_results,
    #     specific_research_results,
    # )

    save_raw_data_file(
        competitor_name=companyName,
        search_results=search_results,
        specific_research_results=specific_research_results,
    )


# STREAMLIT COMPONENTS

def process_data(companyName, websiteName):
    metrics_list_keys = ["Website URL", "Sector", "Industry", "Location", "Number of Employees", "Founding Year", "Company Type", "Market Cap", "Annual Revenue", "LinkedIn URL", "Tagline", "Stock Ticker",]
    competitor_name = companyName
    website = websiteName
    # email_report = write_email_report(competitor_name)
    metrics_data_raw = get_metrics_data(
        competitor_name, website, metrics_list_keys
    )
    metrics_data = utils.parse_json_output(metrics_data_raw)
    # metrics_data = {
    #     "website": "http://www.microsoft.com",
    #     "sector": "Technology",
    #     "industry": "Software and Video Games",
    #     "location": "Redmond, Washington, USA",
    #     "number_of_employees": 221000,
    #     "founding_year": 1975,
    #     "company_type": "Public",
    #     "market_cap": None,
    #     "annual_revenue": "US$110.36 billion (2018)",
    #     "linkedin_url": None,
    #     "tagline": "Empower every person and every organization on the planet to achieve more.",
    #     "stock_ticker": "MSFT",
    #     "competitor_name": "Microsoft",
    # }
    
    save_metrics_data_file(metrics_data,competitor_name, metrics_list_keys)
    return None


def get_metrics_data(competitor_name, website, metrics_list_keys):
    metrics_parsing_agent = Agent(
        prompt_persona="You are intelligent agent that can process raw text data into structured JSON format. Please provide the information in plain JSON format without any additional characters or markdown. Return ONLY the JSON object. If a matching value for a key is not found, let the value be None.",
        role="Metrics Parser",
    )

    search_task = Task(
        name="Metrics data search",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=perplexity_model_text,
        instructions=f"I need recent and updated information about the company {competitor_name} - {website}. Please search and provide comprehensive insights based on the following details required: {metrics_list_keys}.",
        log_output=True,
    ).execute()

    metrics_parsing_task = Task(
        name="Metrics Parsing Task",
        agent=metrics_parsing_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions=f"Use the company information provided and return the information as a JSON object with keys for : {metrics_list_keys}",
        log_output=True,
        enhance_prompt=False,
        previous_output=search_task,
        input_tasks=[search_task],
    ).execute()

    return metrics_parsing_task


# def write_email_report(company_name):
#     memory_file_path = f"raw_data_files/{company_name}.txt"
#     email_writer_memory = OpenAIMemory(file_path=memory_file_path)

#     email_writer_agent = Agent(
#         prompt_persona="""You are intelligent agent that can generate a comprehensive summary using the latest information provided about a company. Ensure the summary is organized, succinct, and tailored to the specified audience. Use clear section headings and maintain the requested tone throughout the document.
#         Target Audience - Competitor of the company
#         Tone and Style - Formal and informative
#         Summary Format - 
#         1. Company Name: [Name of the Company]
#         2. Key Events:
#         Article 1: [Title]
#         [Published Date]
#         [2 bullet points to summarize article 1]
#         Article 2: [Title]
#         [Published Date]
#         [2 bullet points to summarize article 2]
#         ...
#         3. General Research: [Summary of General Research]
#         IF Specific Research section is present,
#             4. Specific Research: [Summary of Specific Reseach]
#         """,
#         role="Competitor Analyst",
#         memory=email_writer_memory,
#     )

#     content_writer_task = Task(
#         name="Competitor Analyst Task",
#         agent=email_writer_agent,
#         output_type=OutputType.TEXT,
#         input_type=InputType.TEXT,
#         model=open_ai_model_text,
#         instructions=f"Use the articles provided about the company {company_name} and write a summary for each and every article. Each article starts with 'Title:', followed by the content. If Specific Research or General Research is present, write a summary about them. If Specific Research or General Research is NOT present, do not generate anything. Send the response in text without any markdown. Use bullets for points and beautify it be as creative as you want",
#         log_output=True,
#         enhance_prompt=False,
#     ).execute()

#     return content_writer_task



def save_metrics_data_file(metrics_data, competitor_name, metric_keys):
    FILE_NAME = os.path.join(FOLDER_NAME, competitor_name + ".txt")
    metrics_dict = metric_keys
    with open(FILE_NAME, "a") as my_file:
        my_file.write(f"\n\nMetrics about the company {competitor_name}:\n")
        for key, value in metrics_data.items():
            if key in list(metrics_dict):
                my_file.write(key + ": " + str(value) + "\n")
            else:
                my_file.write(key + ": " + str(value) + "\n")


# STREAMLIT COMPONENTS
# try:
#     document_id = st.session_state["document_id"]
# except:
#     st.error("Please complete Initiate Research step!")
#     st.stop()

# st.header("View your research data")

# result1 = competitors_list_collection.find_one({"_id": document_id})
# competitors_list = result1["generated_competitors_list"]

# result2 = base_research_collection.find(
#     {"competitors_list_document_id": document_id},
#     {"raw_data": 1, "competitor_name": 1},
# )

# object_id_column = []
# competitor_name_column = []
# raw_data_column = []
# website_column = []

# for item in result2:
#     object_id_column.append(item["_id"])
#     competitor_name_column.append(item["competitor_name"])
#     raw_data_column.append(item["raw_data"])
#     website_column.append(competitors_list[item["competitor_name"]])

# dataframe_dict = {
#     "id": object_id_column,
#     "competitor_name": competitor_name_column,
#     "website": website_column,
#     "raw_data": raw_data_column,
# }
# df = pd.DataFrame(dataframe_dict)
# df.index = df.index + 1
# st.dataframe(df, column_config={"id": None})

# st.write("## Generate report for")
# generate_report_list = st.multiselect(
#     "Generate Report for", options=competitor_name_column, label_visibility="collapsed"
# )

# fields = [
#     "Website URL",
#     "Sector",
#     "Industry",
#     "Location",
#     "Number of Employees",
#     "Founding Year",
#     "Company Type",
#     "Market Cap",
#     "Annual Revenue",
#     "LinkedIn URL",
#     "Tagline",
#     "Stock Ticker",
# ]
# st.write("## Select required metrics")
# metrics_list_values = [field for field in fields if st.checkbox(field, value=True)]

# report_button = st.button("Generate report")
# if report_button:
#     if metrics_list_values:
#         metrics_dict = {}
#         for name in metrics_list_values:
#             key_value = utils.convert_field_name_advanced(name.strip())
#             metrics_dict[key_value] = name.strip()

#         st.session_state.metrics_dict = metrics_dict
#     else:
#         st.error("No fields selected.")
#     filtered_dataframe = df[df["competitor_name"].isin(generate_report_list)]
#     filtered_dataframe.apply(
#         process_data,
#         axis=1,
#         args=(document_id,),
#     )

#     st.write(
#         """
#         # Report generated! :sparkles:
#         ### Go to :red[Access Reports] Page"""
#     )
#     st.page_link("pages/2_Access_Reports.py", label="Access Reports", icon="📁")
#     st.write("### To chat with the data, go to :red[Chat With Knowledge Base] page")
#     st.page_link(
#         "pages/3_Chat_With_Knowledge_Base.py",
#         label="Chat With Knowledge Base",
#         icon="🤖",
#     )