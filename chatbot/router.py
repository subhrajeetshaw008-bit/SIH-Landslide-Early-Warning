def route_query(user_query):

    query = user_query.lower().strip()

    # Weather Questions
    if any(word in query for word in [
        "weather",
        "temperature",
        "humidity",
        "rainfall",
        "wind speed",
        "wind"
    ]):
        return {
            "type": "weather"
        }

    # Risk / Prediction Questions
    elif any(phrase in query for phrase in [
        "risk score",
        "landslide risk",
        "risk level",
        "susceptibility",
        "calculate risk",
        "predict risk",
        "risk prediction"
    ]):
        return {
            "type": "risk"
        }

    # News Questions
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

    # Everything Else → Mistral
    return {
        "type": "mistral"
    }