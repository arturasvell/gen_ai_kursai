import ollama

def get_topic(text: str) -> str:
    prompt = f"""Determine the single most relevant topic for the following text. 
    The topic should be a single word or a short phrase. 
    Examples: 'Science', 'History', 'Technology', 'Art', 'Sports'.

    Text: "{text}"

    Topic:"""

    response = ollama.generate(
        model="gemma3",
        prompt=prompt,
        stream=False
    )
    topic = response.get('response', 'unknown_topic').strip()
    return topic
