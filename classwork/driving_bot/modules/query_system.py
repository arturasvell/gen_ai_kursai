from .embedding import query
from .llm_setup import get_driving_answer, validate_driving_question


def ask_driving_question(question: str, collection):
    print(f"Validating question relevance...")
    
    # First validate if the question is related to Lithuanian driving rules
    is_relevant = validate_driving_question(question)
    
    if not is_relevant:
        return "I'm sorry, but I can only answer questions related to Lithuanian traffic rules and driving regulations. Please ask a question about Lithuanian driving laws, traffic signs, road safety, or similar topics."
    
    print(f"Searching for relevant traffic rules...")
    
    result = query(question, collection)
    
    if not result['documents'] or not result['documents'][0]:
        return "I couldn't find relevant information about that in the Lithuanian traffic rules."
    
    context = "\n".join(result['documents'][0])
    
    print(f"Found relevant rules. Generating answer...")
    
    answer = get_driving_answer(question, context)
    
    if answer is None:
        return "Sorry, I encountered an error while processing your question."
    
    return answer


def interactive_query(collection):
    print("Welcome to the Lithuanian Traffic Rules Assistant!")
    print("Ask me any question about Lithuanian traffic rules. Type 'exit' to quit.")
    print("Note: I can only answer questions related to Lithuanian driving laws and traffic regulations.")
    
    while True:
        question = input("\nYour question: ")
        
        if 'exit' in question.lower():
            print("Goodbye!")
            break
        
        if not question.strip():
            print("Please enter a question.")
            continue
        
        answer = ask_driving_question(question, collection)
        print(f"\nAnswer: {answer}") 