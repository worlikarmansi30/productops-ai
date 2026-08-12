import chromadb

from embed import embed_documents


# Create persistent ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")


# Create or load collection
collection = client.get_or_create_collection(
    name="product_documents"
)


def store_documents():

    # Get chunks + embeddings from embed.py
    document_chunks = embed_documents()

    print(f"Number of chunks to store: {len(document_chunks)}")

    for chunk in document_chunks:

        chunk_id = f"{chunk['source']}_{chunk['chunk_id']}"

        collection.upsert(
            ids=[chunk_id],
            documents=[chunk["text"]],
            embeddings=[chunk["embedding"]],
            metadatas=[
                {
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"]
                }
            ]
        )

    print(f"Documents stored successfully.")
    print(f"Total vectors in ChromaDB: {collection.count()}")


if __name__ == "__main__":
    store_documents()