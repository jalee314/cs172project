from flask import Flask, request, render_template, session, redirect, url_for
from datetime import timedelta, datetime

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
    
    if request.method == 'POST':
        # Input from HTML form
        query = request.form['searchbar']
        # Store the query with the current timestamp
        session[query] = str(datetime.now())  # Store as ISO string for JSON serializability

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
                           response_data = example_data,
                           current_query = query)