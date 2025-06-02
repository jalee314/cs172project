import lucene
import os
import json
import argparse
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, StringField, NumericDocValuesField, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import NIOFSDirectory

def create_index(index_dir, data_dir):
    
    #index_dir is where outputted indexes will be stored, data_dir is directory where json files are  held

    if not os.path.exists(index_dir):
        os.makedirs(index_dir)

    storedir = NIOFSDirectory(Paths.get(index_dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE) 
    writer = IndexWriter(storedir, config)

    
    #for text that needs to be tokenized and indexed for searching
    text_field_type = FieldType()
    text_field_type.setStored(True)
    text_field_type.setTokenized(True)
    text_field_type.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS) #For phrase queries

    #for string fields that should be indexed as a single token (e.g., IDs, exact categories)
    string_field_type = FieldType()
    string_field_type.setStored(True)
    string_field_type.setTokenized(False) #index as a single token
    string_field_type.setIndexOptions(IndexOptions.DOCS) #check if it exists in the doc 


    print(f"Indexing data from {data_dir} into {index_dir}.")

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"): #
            filepath = os.path.join(data_dir, filename) #path looks like ../output_dir/output_n.json
            print(f"Processing file: {filepath}")
            with open(filepath, 'r') as f:
                for line_number, line in enumerate(f):
                    try:
                        reddit_post = json.loads(line.strip()) 
                        doc = Document()

                        doc.add(Field('id', str(reddit_post['id']), string_field_type))                         
                        doc.add(Field('title', str(reddit_post['title']), text_field_type))                         
                        doc.add(Field('selftext', str(reddit_post['selftext']), text_field_type))
                        doc.add(Field('author', str(reddit_post['author']), string_field_type))
                        doc.add(Field('subreddit', str(reddit_post['subreddit']), string_field_type))                        
                        doc.add(Field('permalink', str(reddit_post['permalink']), string_field_type))                        
                        doc.add(Field('url', str(reddit_post['url']), string_field_type))
                        if reddit_post.get('linked_page_title'):
                            doc.add(Field('linked_page_title', reddit_post['linked_page_title'], text_field_type)) 
                        
                        #index created_utc as a numeric field for sorting/range queries, convert from float to an int from slide 7 
                        timestamp = int(float(reddit_post['created_utc'])) 
                        doc.add(NumericDocValuesField('created_utc', timestamp))

                        #index comments as a single text field by joining them
                        comments_list = reddit_post.get('comments', [])  
                        if comments_list: 
                            all_comments = " ".join(comments_list)
                            doc.add(Field('comments', all_comments, text_field_type))
                        
                        writer.addDocument(doc)

                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in {filename} at line {line_number + 1}: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred while processing {filename} at line {line_number + 1}: {e}")

    print(f"Finished indexing. Closing writer.")
    writer.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Index Reddit data using PyLucene.")
    parser.add_argument('-i', '--index_dir',default="reddit_index",type=str,help="Directory to store the Lucene index (default: reddit_index)")
    parser.add_argument('-d', '--data_dir',default="output_files",type=str,help="Directory containing JSON data files from the crawler (default: output_files)")
    args = parser.parse_args()

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    INDEX_DIRECTORY = args.index_dir
    DATA_DIRECTORY = args.data_dir

    if not os.path.exists(DATA_DIRECTORY) or not os.listdir(DATA_DIRECTORY):
        print(f"Data directory '{DATA_DIRECTORY}' does not exist or is empty.")
        print("Please run your crawler first to generate data, or ensure the path is correct.")
    else:
        create_index(INDEX_DIRECTORY, DATA_DIRECTORY)
        print(f"Index created in '{INDEX_DIRECTORY}' directory.")
