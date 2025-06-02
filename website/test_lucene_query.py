from lucene_query import search_index

query = "example query"
results = search_index(query)

for result in results:
    print(f"Rank: {result['rank']}, Title: {result['title']}, Upvotes: {result['upvotes']}")