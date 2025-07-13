import chromadb
from embedding import get_embedding, get_embeddings

def init_chroma():
    client = chromadb.PersistentClient(path="./vector-db")
    return client

def get_or_create_collection(client, topic):
    collection = client.get_or_create_collection(topic)
    return collection

def add_to_collection(collection, chunks, metadata):
    chunks_text = [chunk.page_content for chunk in chunks]
    embedding_collection = get_embeddings(chunks_text)
    for i in range(0, len(embedding_collection)):
        collection.upsert(documents=chunks_text[i],
                         ids=[f"fact-{i+1}"],
                         metadatas=[metadata],
                         embeddings = [embedding_collection[i].embedding])

def get_collection(client, topic):
    return client.get_collection(topic)

def query_collection(collection, question):
    question_embedding = get_embedding(question)
    results = collection.query(query_embeddings=[question_embedding.embedding], n_results=1)
    return results

def list_collections(client):
    return client.list_collections()
