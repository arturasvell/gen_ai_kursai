from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import re

def get_chunks_of_text(text: str, chunk_size: int, chunk_overlap: int):
    document = Document(page_content=text)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_documents(documents=[document])

    return chunks

def sanitize_topic(topic: str) -> str:
    topic = topic.replace(" ", "_")
    topic = re.sub(r'[^a-zA-Z0-9_-]', '', topic)
    return topic[:50]
