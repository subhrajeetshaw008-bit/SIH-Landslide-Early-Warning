import os

from dotenv import load_dotenv

from tavily import TavilyClient

load_dotenv()

client = TavilyClient(
    api_key=os.getenv(
        "TAVILY_API_KEY"
    )
)

def search_web(query):
    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
    except Exception:
        return []

    return response["results"]