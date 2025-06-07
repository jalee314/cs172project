import lucene
from java.nio.file import Paths
from java.lang import Float
from java.util import HashMap

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser

def search_reddit_index(index_dir, query, top_k=10):  

    lucene.getVMEnv().attachCurrentThread()
  
    storedir = NIOFSDirectory(Paths.get(index_dir))
    searcher = IndexSearcher(DirectoryReader.open(storedir))

    # Using boosting for different fields, order of priority title > selftext > comments > linked_page_title
    fields = ["title", "selftext", "comments", "linked_page_title"]
    boost_map = HashMap()
    boost_map.put("title", Float(3.0))              
    boost_map.put("selftext", Float(2.0))           
    boost_map.put("comments", Float(1.5))
    boost_map.put("linked_page_title", Float(1.0))

    # Parse it BM25 (we can change it if you want to use a different scoring model)
    parser = MultiFieldQueryParser(fields, StandardAnalyzer(), boost_map)
    parsed_query = MultiFieldQueryParser.parse(parser, query)

    hits = searcher.search(parsed_query, top_k).scoreDocs
    topkdocs = []

    # Convert document object to a list of dictionaries
    for hit in hits:
        doc = searcher.doc(hit.doc)

        # # Higher score if more upvotes
        score = hit.score # Default BM25
        upvotes_str = doc.get("upvotes")
        upvotes = int(upvotes_str) if upvotes_str else 0
        final_score = score + 0.005 * upvotes	# small boost for upvotes when scores are similar

        topkdocs.append({
            "score": final_score,
            "title": doc.get("title"),
            "upvotes": doc.get("score"),
            "selftext": doc.get("selftext")[:100] + "..." if doc.get("selftext") else "",
            "comments": doc.get("comments")[:100] + "..." if doc.get("comments") else "",
            "linked_page_title": doc.get("linked_page_title")[:100] + "..." if doc.get("linked_page_title") else "",
            "subreddit": doc.get("subreddit"),
            "permalink": doc.get("permalink")
        })

    return topkdocs

