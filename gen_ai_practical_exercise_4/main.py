from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
import os
import google.genai as genai
from text_processing import get_chunks_of_text, sanitize_topic
from vector_db import init_chroma, get_or_create_collection, add_to_collection, query_collection, get_collection, list_collections
import ollama
from topic_modeling import get_topic
from database import init_db, add_log_entry, get_log_entries
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Text Ingestion API",
    description="An API to ingest text, determine its topic, and store it in a vector database.",
    version="1.0.0",
)

class LogEntry(BaseModel):
    id: int
    topic: str
    collection_name: str
    creation_date: str

init_db()
chroma_client = init_chroma()
GOOGLE_AI_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_AI_KEY)

@app.get("/logs", summary="Get Ingestion Logs", description="Retrieve the last 100 ingestion log entries from the database.", response_model=List[LogEntry])
def get_logs():
    return get_log_entries()

@app.post("/ingest", summary="Ingest Text", description="Ingest text, determine its topic, chunk it, and store it in a vector database.")
async def ingest_data(
    text: str = Form(...),
    chunk_size: int = Form(1000),
    overlap: int = Form(200),
    metadata: Optional[str] = Form(None),
):
    parsed_metadata = None
    if metadata:
        try:
            parsed_metadata = json.loads(metadata)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format for metadata.")

    topic = get_topic(text)
    collection_name = sanitize_topic(topic)
    if len(collection_name) < 3:
        collection_name = "general"

    collection = get_or_create_collection(chroma_client, collection_name)
    chunks = get_chunks_of_text(text, chunk_size, overlap)
    add_to_collection(collection, chunks, parsed_metadata)
    add_log_entry(topic, collection_name)
    return {"message": f"Text has been chunked and stored in the '{collection_name}' collection."}

@app.get("/search", summary="Search for Information", description="Ask a question and get a response from the embedded Chroma DB. The response will be in Lithuanian.")
async def search(question: str):
    topic = get_topic(question)
    collection_name = sanitize_topic(topic)
    if len(collection_name) < 3:
        collection_name = "general"

    try:
        collection = get_collection(chroma_client, collection_name)
    except Exception as e:
        collections = list_collections(chroma_client)
        if not collections:
            return {"error": "No collections found."}
        
        collection_names = [col.name for col in collections]

        prompt = f"""Given the user's question, which of the following collections is most likely to contain the answer?
        Question: {question}
        Collections: {', '.join(collection_names)}
        
        Respond with only the single most relevant collection name.
        """
        response = ollama.generate(
            model="gemma3",
            prompt=prompt,
            stream=False
        )
        collection_name = response.get('response', '').strip()
        
        if not collection_name or collection_name not in collection_names:
            return {"error": f"Could not determine a relevant collection to search."}
        
        try:
            collection = get_collection(chroma_client, collection_name)
        except Exception as e:
            return {"error": f"Collection for topic '{collection_name}' not found after attempting to find a relevant one."}

    results = query_collection(collection, question)
    
    context = ""
    if results and results['documents']:
        context = "\n".join(results['documents'][0])

    if not context:
        return {"response": "Atsiprašome, informacijos nerasta."}

    prompt = f'''Atsakykite į klausimą lietuviškai, remdamiesi šiuo kontekstu:

Context: {context}

Question: {question}

Answer:'''

    response = client.models.generate_content(
        model=f"models/gemini-1.5-flash",
        contents=prompt,
    )

    return {"response": response.text}
