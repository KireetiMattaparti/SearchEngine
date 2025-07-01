from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import pandas as pd

# Load cleaned data
cleaned_data = pd.read_csv("cleaned_data.csv")

# Initialize Sentence Transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Initialize Elasticsearch
es = Elasticsearch(["https://localhost:9200"],basic_auth=("elastic", "QXv9RC0slqs8Qe1=0yJT"), verify_certs=True,ca_certs= r"C:\Users\kiree\OneDrive\Desktop\elasticsearch-8.13.0\config\certs\http_ca.crt")

# Clear existing index
es.indices.delete(index='movie_embeddings', ignore=[400, 404])

# Embed and store data
for index, row in cleaned_data.iterrows():
    text_to_embed = row['clean_text']
    embedding = model.encode(text_to_embed)
    doc = {
        "Series_Title": row["Series_Title"],
        "Overview": row["Overview"],
        "embedding": embedding.tolist()
    }
    # Index the document in Elasticsearch
    es.index(index="movie_embeddings", body=doc)
