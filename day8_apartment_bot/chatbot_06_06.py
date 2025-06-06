import os
import requests
import json
from requests.exceptions import RequestException
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.0-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
SYSTEM_PROMPT = "You are an expert on improving apartments. If the user asks anything outside that domain, answer: \"Sorry, I don't have knowledge on that.\" Wait for a new question."
ON_TOPIC_KEYWORDS = ["apartment", "flat", "room", "renovation", "furniture", "storage", "decor"]
FINISH_KEYWORDS = ["stop", "exit"]

def is_question_on_topic(question: str) -> bool:
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in ON_TOPIC_KEYWORDS)

def is_exit_requested(question: str)->bool:
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in FINISH_KEYWORDS)   


def send_question_to_gemini(question: str):
    print("Sending API call to Google Gemini...")
    headers = {
        "Content-Type": "application/json",
    }
        
    body = {
        "system_instruction": {
             "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": [{
             "role": "user",
            "parts": [{"text": question}]
        }],
        "generationConfig": {
            "temperature": 0.7
        }
    }
        
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(body), timeout=20)
        response.raise_for_status()
            
        api_response = response.json()
            
        if "candidates" in api_response and api_response["candidates"]:
            reply_from_gemini = api_response["candidates"][0]["content"]["parts"][0]["text"]
        else:
            reply_from_gemini = "I'm sorry, I couldn't generate a response for that."
            
        print(f"\n GEMINI: {reply_from_gemini}")

    except RequestException as e:
        print(f"An error occurred with the API call: {e}")
        if e.response:
            print(f"Error message: {e.response.text}")  

def ask_apartment_bot(question: str) -> None:
    if not is_question_on_topic(question):
        print("Your question is off-topic. Responding without API call.")
        print("\nGEMINI: Sorry, I don't have knowledge on that.")
        return
    
    send_question_to_gemini(question)
    

print("Hello. I am GEMINI. Please ask me questions related to apartments.")

while True:
    user_question = input("\nPlease enter your question: ")
    if is_exit_requested(user_question):
        print("Exit request received. Stopping the program.")
        break
    
    ask_apartment_bot(user_question)