import os

from dotenv import load_dotenv

load_dotenv()

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

api_key = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=api_key) if TavilyClient and api_key else None

def search_web(query):
    if client is None:
        return []

    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
    except Exception:
        return []

    return response["results"]