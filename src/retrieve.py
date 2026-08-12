import chromadb

from embed import create_embedding


# Connect to the existing ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Get the collection we already created
collection = client.get_collection(
    name="product_documents"
)


def retrieve(query, top_k=2):

    # Convert the user's question into an embedding
    query_embedding = create_embedding(query)

    # Ask ChromaDB for the most similar chunks
    results = collection.query(
    query_embeddings=[query_embedding],
    n_results=top_k,
    include=["documents", "metadatas", "distances"]
)

    retrieved_chunks = []

    MAX_DISTANCE = 1.2

    for i in range(len(results["documents"][0])):
        distance = results["distances"][0][i]

        if distance <= MAX_DISTANCE:
            retrieved_chunks.append({
                "score": distance,
                "distance": distance,
                "chunk": {
                    "text": results["documents"][0][i],
                    "source": results["metadatas"][0][i]["source"],
                    "chunk_id": results["metadatas"][0][i]["chunk_id"]
                }
            })

    return retrieved_chunks


if __name__ == "__main__":

    query = "What does PRD-205 say about payment failures?"

    results = retrieve(query)

    print("\nQUERY:")
    print(query)

    print("\nTOP MATCHING CHUNKS:")

    for result in results:
        print("\n--------------------")
        print(f"Source: {result['chunk']['source']}")
        print(f"Chunk ID: {result['chunk']['chunk_id']}")
        print(f"Distance: {result['score']}")
        print(result["chunk"]["text"])