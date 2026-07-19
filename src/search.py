from ddgs import DDGS

import random

def get_live_news_context(sport_name):
    topics = [
        "latest tournament results 2026",
        "recent news updates",
        "records broken history",
        "famous matches legendary players",
        "championship winners cup",
        "rules and strategies"
    ]
    random_topic = random.choice(topics)
    search_query = f"{sport_name} {random_topic}"
    retrieved_texts = []

    print(f"Executing web search for: '{search_query}'...")
    try:
        # Initializing DuckDuckGo search context
        with DDGS() as ddgs:
            # We fetch the top 3 text search results
            results = ddgs.text(search_query, max_results=3)
            
            print(f"Retrieved {results} results from DuckDuckGo.")
            for index, r in enumerate(results, start=1):
                title = r.get("title", "No Title")
                snippet = r.get("body", "No Snippet Content Available")
                retrieved_texts.append(f"Web Source {index}: {title}\nSnippet: {snippet}")

    except Exception as e:
        print(f"Web Search fell back or failed: {e}")
        return "No recent search engine updates available due to system connectivity."

    return "\n\n".join(retrieved_texts)