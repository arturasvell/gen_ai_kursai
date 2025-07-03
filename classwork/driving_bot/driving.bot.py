from modules.embedding import embed_driving_rules
from modules.llm_setup import setup_llm
from modules.query_system import interactive_query

def main():
    print("Starting driving bot setup...")
    
    print("Setting up LLM...")
    setup_llm()
    
    print("Embedding driving rules into ChromaDB...")
    client, collection = embed_driving_rules()
    
    print("Driving rules successfully embedded into ChromaDB!")
    print(f"Collection name: {collection.name}")
    
    print("\nStarting interactive query system...")
    interactive_query(collection)
    
    return client, collection

if __name__ == "__main__":
    main()
