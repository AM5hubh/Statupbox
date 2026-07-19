from ddgs import DDGS

def get_live_news_context(sport_name):
    search_query = f"{sport_name} latest tournament results championship winners news 2026"
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