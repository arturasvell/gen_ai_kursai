import os
from openai import OpenAI
from requests.exceptions import RequestException
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GITHUB_API_KEY") 
MODEL_NAME = "openai/gpt-4.1-nano"
API_URL = "https://models.github.ai/inference"
SYSTEM_PROMPT = "You are an expert on improving apartments. If the user asks anything outside that domain, answer: \"Sorry, I don't have knowledge on that.\" Wait for a new question."
ON_TOPIC_KEYWORDS = ["apartment", "flat", "room", "renovation", "furniture", "storage", "decor"]
FINISH_KEYWORDS = ["stop", "exit"]

def is_question_on_topic(question: str) -> bool:
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in ON_TOPIC_KEYWORDS)

def is_exit_requested(question: str) -> bool:
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in FINISH_KEYWORDS)

def send_question_to_openai(question: str):
    print("Sending API call to ChatGPT...")
    
    try:
        client = OpenAI(base_url=API_URL, api_key=API_KEY)
        response = client.chat.completions.create(
            temperature=0.7,
            messages=[
                {"role": "developer", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ], 
            model=MODEL_NAME, timeout = 20)
        
        api_response = response
        
        if api_response.choices:
            reply_from_chatgpt = api_response.choices[0].message.content
        else:
            reply_from_chatgpt = "I'm sorry, I couldn't generate a response for that."
            
        print(f"\n ChatGPT: {reply_from_chatgpt}")

    except RequestException as e:
        print(f"An error occurred with the API call: {e}")
        if e.response:
            print(f"Error message: {e.response.text}")

def ask_apartment_bot(question: str) -> None:
    if not is_question_on_topic(question):
        print("Your question is off-topic. Responding without API call.")
        print("\n ChatGPT: Sorry, I don't have knowledge on that.")
        return
    
    send_question_to_openai(question)

print("Hello. I am ChatGPT. Please ask me questions related to apartments.")

while True:
    user_question = input("\nPlease enter your question: ")
    if is_exit_requested(user_question):
        print("Exit request received. Stopping the program.")
        break
    
    if not API_KEY:
        print("Error: GITHUB_API_KEY environment variable not set.")
        break

    ask_apartment_bot(user_question)