import lucene
from lucene import (
    SimpleFSDirectory, File, Document, Field, FieldType,
    StandardAnalyzer, IndexWriter, IndexWriterConfig, Version,
    IndexOptions
)

# Initialize JVM
lucene.initVM()

# Define directory for the index
index_dir = SimpleFSDirectory(File("reddit_index"))

# Define the analyzer (used for tokenized fields)
analyzer = StandardAnalyzer()

# Configure the index writer
config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
writer = IndexWriter(index_dir, config)

# Define field types
not_tokenized_stored = FieldType()
not_tokenized_stored.setStored(True)
not_tokenized_stored.setTokenized(False)
not_tokenized_stored.setIndexOptions(IndexOptions.DOCS)

tokenized_stored = FieldType()
tokenized_stored.setStored(True)
tokenized_stored.setTokenized(True)
tokenized_stored.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

tokenized_not_stored = FieldType()
tokenized_not_stored.setStored(False)
tokenized_not_stored.setTokenized(True)
tokenized_not_stored.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

# Sample data (replace with your actual content)
sample_doc = {
    "id": "t3_xyz123",
    "author": "user_abc",
    "created_utc": "1653916800",
    "title": "Lucene Indexing in Python",
    "selftext": "This is a detailed explanation of how Lucene fields work.",
    "score": "128",
    "url": "https://reddit.com/r/example/t3_xyz123",
    "permalink": "/r/example/comments/xyz123/",
    "comments": "Great explanation! Very helpful."
}

# Create document
doc = Document()
doc.add(Field("id", sample_doc["id"], not_tokenized_stored))
doc.add(Field("author", sample_doc["author"], not_tokenized_stored))
doc.add(Field("created_utc", sample_doc["created_utc"], not_tokenized_stored))
doc.add(Field("title", sample_doc["title"], tokenized_stored))
doc.add(Field("selftext", sample_doc["selftext"], tokenized_not_stored))
doc.add(Field("score", sample_doc["score"], not_tokenized_stored))
doc.add(Field("url", sample_doc["url"], not_tokenized_stored))
doc.add(Field("permalink", sample_doc["permalink"], not_tokenized_stored))
doc.add(Field("comments", sample_doc["comments"], tokenized_not_stored))

# Add the document to the index
writer.addDocument(doc)

# Commit and close
writer.commit()
writer.close()

print("Indexing complete.")
