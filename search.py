import streamlit as st
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import numpy as np

# Initialize Sentence Transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Initialize Elastic
# search
es = Elasticsearch("https://localhost:9200",basic_auth=("elastic", "QXv9RC0slqs8Qe1=0yJT"),
    verify_certs=True,
    ca_certs=r"C:\Users\kiree\OneDrive\Desktop\elasticsearch-8.13.0\config\certs\http_ca.crt")

# function to embed text
def embed_text(text):
    return model.encode(text)

# function to search Elasticsearch
def search(query_embedding):
    #  Elasticsearch query
    search_query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            }
        }
    }
    
    # Execute Elasticsearch query
    response = es.search(index="movie_embeddings", body=search_query)
    hits = response['hits']['hits']

    # Extract movie name and overview from search results
    search_results = []
    for hit in hits:
        search_result = {}
        search_result['Series_Title'] = hit['_source']['Series_Title']
        search_result['Overview'] = hit['_source']['Overview']
        search_results.append(search_result)
    
    # Return search results
    return search_results

# Create Streamlit app
def main():
    st.title("Semantic Search App")
    # Reads an input from the user
    user_input = st.text_input("Enter your query:")
    if user_input:
        # Embed the input
        query_embedding = embed_text(user_input)
        # Search the vector DB for the entries closest to the user input
        search_results = search(query_embedding)
        # Outputs/displays the closest entries found
        st.write("Search Results:")
        for search_result in search_results:
            st.markdown(f"**{search_result['Series_Title']}**")
            st.info(search_result['Overview'])
            st.write("\n")

if __name__ == "__main__":
    main()
