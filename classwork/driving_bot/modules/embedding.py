from ollama import embeddings
import chromadb
from .data_collector import read_source_file, get_chunks_of_text


def get_embedding(text):
    return embeddings(model='nomic-embed-text', prompt=text)


def get_embeddings(text_list):
    result = []
    for text in text_list:
        result.append(get_embedding(text))
    return result


def init_chroma():
    client = chromadb.PersistentClient(path="./vector-db")
    collection = client.get_or_create_collection("driving_rules")
    return (client, collection)


def embed_driving_rules():
    text = read_source_file()
    chunks = get_chunks_of_text(text)
    chunks_text = [chunk.page_content for chunk in chunks]
    
    (chroma_client, chroma_collection) = init_chroma()
    embedding_collection = get_embeddings(chunks_text)
    
    for i in range(0, len(embedding_collection)):
        chroma_collection.upsert(
            documents=chunks_text[i],
            ids=[f"rule-{i+1}"],
            embeddings=[embedding_collection[i].embedding]
        )
    
    return (chroma_client, chroma_collection)


def query(input: str, collection: chromadb.Collection):
    embedded_query = get_embedding(input)
    result = collection.query(
        query_embeddings=[embedded_query.embedding], 
        n_results=2
    )
    return result 