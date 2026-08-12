import os
from dotenv import load_dotenv
from openai import OpenAI

from ingest import load_documents
from chunk import chunk_text

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def create_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def embed_documents():
    docs = load_documents()
    print(f"DEBUG: Documents loaded = {len(docs)}")

    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        print(f"DEBUG: Chunks created = {len(chunks)}")

        for i, chunk in enumerate(chunks):
            chunk_data = {
                "text": chunk,
                "source": doc["source"],
                "chunk_id": i
            }

            chunk_data["embedding"] = create_embedding(chunk)

            all_chunks.append(chunk_data)

    return all_chunks