from ollama import embeddings

def get_embedding(fact):
    return embeddings(model='nomic-embed-text', prompt=fact)

def get_embeddings(prompt_list):
    result = []
    for fact in prompt_list:
        result.append(get_embedding(fact))
    return result

