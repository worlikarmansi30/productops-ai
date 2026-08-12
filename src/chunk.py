from ingest import load_documents


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks

if __name__ == "__main__":
    docs = load_documents()

    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            chunk_data = {
                "text": chunk,
                "source": doc["source"],
                "chunk_id": i
            }

            all_chunks.append(chunk_data)

    for chunk in all_chunks:
        print("\n--------------------")
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"])