import json

def search_index(query_string, json_file="mock_results.json"):
    print(f"[JSON] Loading search results for query: {query_string}")
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Could not find {json_file}. Returning empty results.")
        return []

    return results