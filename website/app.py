from flask import Flask, request, render_template, session, redirect, url_for
from datetime import timedelta, datetime
#from search import search_reddit_index

app = Flask(__name__)

#needed for the session logic 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#intial page that clears session and routes to the search page 
@app.route('/')
def start():
    session.clear()
    return redirect(url_for('search'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    error = None
    query = ''
    example_data = ''
    example_data_fresh = ''
    
    if request.method == 'POST':
        # Input from HTML form
        query = request.form['searchbar']
        # Store the query with the current timestamp
        session[query] = str(datetime.now())  # Store as ISO string for JSON serializability


        #THIS IS WHERE QUERY AND RESPONSE IS HANDLED 

        #top_k_docs = search_reddit_index('reddit_index', query)


        example_data = [

            {
                "rank": 1,
                "title": "How to learn Python effectively?",
                "upvotes": 152,
                "date": "2025-05-25T14:30:00Z",
                "author": "user123",
                "url": "https://reddit.com/r/learnpython/comments/abc123"
            },
            {
                "rank": 2,
                "title": "Best practices for Flask applications",
                "upvotes": 230,
                "date": "2025-05-20T09:15:00Z",
                "author": "dev_guru",
                "url": "https://reddit.com/r/flask/comments/def456"
            },
            {
                "rank": 3,
                "title": "What's new in JavaScript ES2025?",
                "upvotes": 98,
                "date": "2025-05-27T18:00:00Z",
                "author": "jsfan",
                "url": "https://reddit.com/r/javascript/comments/ghi789"
            }
        ]

        example_data_fresh = [
            {
                "score": 152,
                "title": "How to learn Python effectively?",
                "selftext": "Learning Python effectively requires consistency, practice, and a good curriculum...",
                "comments": "Start with basics, then move to projects and libraries...",
                "linked_page_title": "Python Learning Resources",
                "subreddit": "learnpython",
                "permalink": "/r/learnpython/comments/abc123"
            },
            {
                "score": 230,
                "title": "Best practices for Flask applications",
                "selftext": "Flask is a microframework, and best practices include structuring your app...",
                "comments": "Use blueprints, set up configuration files, avoid global state...",
                "linked_page_title": "Flask Documentation Overview",
                "subreddit": "flask",
                "permalink": "/r/flask/comments/def456"
            },
            {
                "score": 98,
                "title": "What's new in JavaScript ES2025?",
                "selftext": "ES2025 introduces several enhancements including pattern matching, pipeline operator...",
                "comments": "Interesting to see how browsers will adopt these changes...",
                "linked_page_title": "JavaScript ES2025 Features",
                "subreddit": "javascript",
                "permalink": "/r/javascript/comments/ghi789"
            }
        ]

    

    # Convert session items to (query, datetime) tuples
    query_items = [(k,v) for k, v in session.items()]

    # Sort by most recent timestamp (descending)
    sorted_queries = sorted(query_items, key=lambda item: item[1], reverse=True)



    # Extract just the query strings of the 3 most recent
    queries = [item[0] for item in sorted_queries]

    #example data to send and test sorting 
    #change this to be empty, unless the method is post, then update with results 
    



    return render_template('search.html', 
                           error=error,
                           query_list=queries,
                           recent_length = len(queries),
                           response_data = example_data_fresh,
                           current_query = query)
