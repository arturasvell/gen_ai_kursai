import subprocess
import requests
from pydantic import BaseModel


class DrivingResponse(BaseModel):
    answer: str
    rule_reference: str
    confidence: float


def setup_llm():
    model_name = "gemma3"
    print(f"Pulling {model_name} model from Ollama...")
    subprocess.run(["ollama", "pull", model_name], check=True)
    return model_name


def validate_driving_question(question: str) -> bool:
    """
    Validates if a question is related to Lithuanian driving rules.
    Returns True if the question is relevant, False otherwise.
    """
    model_name = "gemma3"
    
    validation_prompt = f"""You are a validation assistant for a Lithuanian traffic rules chatbot. 
    Your task is to determine if a user's question is related to Lithuanian driving rules, traffic laws, road safety, or driving regulations.
    
    Question: "{question}"
    
    Consider the following topics as relevant:
    - Lithuanian traffic rules and laws
    - Road signs and traffic signals
    - Driving licenses and requirements
    - Vehicle registration and technical requirements
    - Road safety and traffic violations
    - Speed limits and traffic regulations
    - Parking rules and restrictions
    - Pedestrian and cyclist rights
    - Emergency vehicles and priority rules
    - Traffic accidents and procedures
    
    Consider the following topics as NOT relevant:
    - General questions about other countries' traffic rules
    - Questions about cooking, sports, entertainment, etc.
    - Personal advice unrelated to driving
    - Questions about other legal areas (criminal law, civil law, etc.)
    - Technical questions about vehicle mechanics (unless related to legal requirements)
    
    Respond with only "YES" if the question is related to Lithuanian driving rules, or "NO" if it's not.
    Be strict - only answer "YES" if the question clearly relates to Lithuanian traffic rules or driving regulations."""
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": validation_prompt,
                "stream": False
            },
            timeout=10
        )
        
        if not response.ok:
            print(f"Validation error: {response.status_code}")
            return True  # Default to accepting if validation fails
        
        result = response.json()["response"].strip().upper()
        return result == "YES"
        
    except Exception as e:
        print(f"Validation error: {e}")
        return True  # Default to accepting if validation fails


def get_driving_answer(question: str, context: str):
    model_name = "gemma3"
    
    prompt = f"""You are a helpful assistant that answers questions about Lithuanian traffic rules. 
    Use the following context to answer the question accurately and concisely.
    
    Context: {context}
    
    Question: {question}
    
    Please provide a clear answer based on the Lithuanian traffic rules provided in the context."""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
    )

    if not response.ok:
        print("Error:", response.status_code)
        return None
    
    return response.json()["response"] 