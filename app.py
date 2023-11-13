import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import json
from pydantic import BaseModel
from fastapi import FastAPI

load_dotenv()
brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")



# 2. Tool for scraping
def scrape_website( url: str):
    
    print("Scraping website...")
    # Define the headers for the request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }

    # Define the data to be sent in the request
    data = {
        "url": url
    }

    # Convert Python object to JSON string
    data_json = json.dumps(data)

    # Send the POST request
    post_url = f"https://chrome.browserless.io/content?token={brwoserless_api_key}"
    response = requests.post(post_url, headers=headers, data=data_json)
    
    # Check the response status code
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        print("CONTENTTTTTT:", text)
        return text
    else:
        print(f"HTTP request failed with status code {response.status_code}")


# 5. Set this as an API endpoint via FastAPI
app = FastAPI()


class Query(BaseModel):
    query: str

@app.post("/")
def researchAgent(query: Query):
    try:
        query = query.query
        content = scrape_website(query)
        
        return content
    except Exception as e:
        raise str(e)
       