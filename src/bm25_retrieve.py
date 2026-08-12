from rank_bm25 import BM25Okapi

from ingest import load_documents
from chunk import chunk_text


def build_bm25_index():

    # Load all documents
    documents = load_documents()

    all_chunks = []

    # Break every document into chunks
    for document in documents:

        chunks = chunk_text(document["text"])

        for i, chunk in enumerate(chunks):

            all_chunks.append({
                "text": chunk,
                "source": document["source"],
                "chunk_id": i
            })

    # Tokenize each chunk for BM25
    tokenized_chunks = [
        chunk["text"].lower().split()
        for chunk in all_chunks
    ]

    # Build BM25 index
    bm25 = BM25Okapi(tokenized_chunks)

    return bm25, all_chunks

def bm25_retrieve(query, top_k=2):

    # Build the BM25 index
    bm25, all_chunks = build_bm25_index()

    # Tokenize the user's question
    tokenized_query = query.lower().split()

    # Calculate BM25 score for every chunk
    scores = bm25.get_scores(tokenized_query)

    # Pair each chunk with its BM25 score
    results = []

    for chunk, score in zip(all_chunks, scores):
        results.append({
            "score": float(score),
            "chunk": chunk
        })

    # Sort from highest score to lowest score
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Return the best matches
    return results[:top_k]

if __name__ == "__main__":

    query = "What does PRD-205 say about payment failures?"

    results = bm25_retrieve(query, top_k=2)

    print("\nQUERY:")
    print(query)

    print("\nTOP BM25 RESULTS:")

    for result in results:
        print("\n--------------------")
        print(f"Source: {result['chunk']['source']}")
        print(f"Chunk ID: {result['chunk']['chunk_id']}")
        print(f"BM25 Score: {result['score']}")
        print(result["chunk"]["text"])