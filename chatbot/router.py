from chatbot.mistral_client import ask_mistral


def route_query(user_query):

    query = user_query.lower()

    # Weather Questions

    if any(word in query for word in [
        "weather",
        "temperature",
        "humidity",
        "rain"
    ]):
        return {
            "type": "weather"
        }

    # Risk Questions

    elif any(phrase in query for phrase in [
        "risk score",
        "risk level",
        "landslide risk",
        "susceptibility",
        "calculate risk",
        "predict risk",
        "risk prediction",
        "current risk",
        "how risky"
    ]):

        return {
            "type": "risk"
        }
    elif any(word in query for word in [
        "news",
        "latest",
        "recent",
        "headlines",
        "what happened"
    ]):
        return {
           "type": "news"
        }

    # Everything Else

    return {
        "type": "mistral"
    }