from chatbot.web_search import (
    search_web
)

from chatbot.mistral_client import (
    ask_mistral
)

def news_response(query):

    results = search_web(
        query
    )

    if not results:
        return "Live news search is unavailable right now. Check that TAVILY_API_KEY is valid, then try again."

    context = ""

    for item in results:

        context += f"""

Title:
{item['title']}

Content:
{item['content']}

"""

    messages = [

        {
            "role": "system",
            "content":
            """
            Summarize the search results clearly.
            Focus on important facts.
            """
        },

        {
            "role": "user",
            "content":
            f"""
            Query:

            {query}

            Search Results:

            {context}
            """
        }
    ]

    return ask_mistral(
        messages
    )