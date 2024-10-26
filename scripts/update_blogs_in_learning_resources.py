"""
This script fetches articles from the DAGWorks blog archive and updates the README file with the latest blog posts.
Before running this script, make sure to install the required packages by running:
pip install -r update_blogs_requirements.txt
"""
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from prompt_toolkit import prompt, HTML
from prompt_toolkit.styles import Style
import argparse

def fetch_articles(url, cutoff_date):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    anchors = soup.find_all('a', class_='_color-pub-primary-text_q8zsn_187')
    timeEls = soup.find_all('time', class_='_date_1v6nm_1')

    #hardcoded blog links
    articles = [
        ("https://pyright.blogspot.com/2024/07/dag-hamilton-workflow-for-toy-text.html", "DAG Hamilton Workflow for Toy Text Processing Script", None),
        ("https://vyom-modi.medium.com/building-a-high-performance-rag-based-ai-with-qdrant-groq-langchain-and-dagworks-hamilton-fb1baa7415bc", "Building a High-Performance RAG-Based AI with Qdrant, Groq, LangChain, and DAGWorks Hamilton", None),
        ("https://blog.getwren.ai/how-do-we-rewrite-wren-ai-llm-service-to-support-1500-concurrent-users-online-9ba5c121afc3", "How do we rewrite Wren AI LLM Service to support 1500 concurrent users online", None)
        ]
    for i, (anchor, time_el) in enumerate(zip(anchors, timeEls)):
        link = anchor['href']
        text = anchor.get_text()

        date_str = time_el['datetime']
        article_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()

        if article_date >= cutoff_date:
            articles.append((link, text, article_date))
            print(f"{len(articles)}: Link: {link}, Text: {text}, Date: {article_date}")

    return articles

def get_cutoff_date():
    style = Style.from_dict({
        'prompt': 'bold',
        'faded': 'ansiblack italic'  
    })

    date_str = prompt(
        HTML('<prompt>Enter cutoff date (YYYY-MM-DD): </prompt>'),
        default=f"{datetime.now().year}-01-01",
        style=style
    )

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return get_cutoff_date() 

def update_readme(articles):
    external_blogs_header = "## 📰 External Blogs\n"
    external_blogs_link = "For the latest blog posts, see the [DAGWorks's Blog](https://blog.dagworks.io/).\n\n"
    blog_entries = []

    for link, text, date in articles:
        if date:
            blog_entries.append(f"* {date} &nbsp;&nbsp; [{text}]({link})")
        else:
            blog_entries.append(f"* [{text}]({link})") 

    new_external_blogs_section = external_blogs_header + external_blogs_link + "\n".join(blog_entries) + "\n"

    with open("readme.md", "r") as file:
        content = file.readlines()

    new_content = []
    in_external_blogs_section = False

    for line in content:
        if line.startswith("## 📰 External Blogs"):
            in_external_blogs_section = True
            new_content.append(new_external_blogs_section)  
        elif in_external_blogs_section and line.startswith("##"):  
            in_external_blogs_section = False

        if not in_external_blogs_section:
            new_content.append(line)  
    with open("readme.md", "w") as file:
        file.writelines(new_content)


def main():
    url = 'https://blog.dagworks.io/archive'
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date", type=str, 
        help="Cutoff date in YYYY-MM-DD format (e.g., 2024-10-01)"
    )
    args = parser.parse_args()

    cutoff_date = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else get_cutoff_date()

    print(f"\n🔍 Fetching articles published after {cutoff_date}...\n")
    articles = fetch_articles(url, cutoff_date)

    print(f"\n✅ Total Articles Fetched: {len(articles)}")
    update_readme(articles)

if __name__ == "__main__":
    main()
