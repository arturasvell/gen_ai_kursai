from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def read_source_file(file_path: str = "data/source.txt") -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def get_chunks_of_text(text: str):
    document = Document(page_content=text)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents=[document])
    return chunks
