from retrieve import retrieve
from bm25_retrieve import bm25_retrieve


def rrf_score(rank, k=60):
    return 1 / (k + rank)


def hybrid_retrieve(query, top_k=2):

    # Get more candidates from each retriever before fusion
    vector_results = retrieve(query, top_k=5)
    bm25_results = bm25_retrieve(query, top_k=5)

    # Dictionary that will hold the combined results
    fused_results = {}

    # STEP 1: Add vector search results
    for rank, result in enumerate(vector_results, start=1):

        chunk = result["chunk"]

        key = (chunk["source"], chunk["chunk_id"])

        fused_results[key] = {
            "chunk": chunk,
            "rrf_score": rrf_score(rank),
            "vector_rank": rank,
            "bm25_rank": None
        }

    # STEP 2: Add BM25 search results
    for rank, result in enumerate(bm25_results, start=1):

        chunk = result["chunk"]

        key = (chunk["source"], chunk["chunk_id"])

        # If vector search already found this chunk,
        # add the BM25 RRF contribution
        if key in fused_results:
            fused_results[key]["rrf_score"] += rrf_score(rank)
            fused_results[key]["bm25_rank"] = rank

        # If BM25 found a new chunk, create a new entry
        else:
            fused_results[key] = {
                "chunk": chunk,
                "rrf_score": rrf_score(rank),
                "vector_rank": None,
                "bm25_rank": rank
            }

    # STEP 3: Rank by combined RRF score
    ranked_results = sorted(
        fused_results.values(),
        key=lambda x: x["rrf_score"],
        reverse=True
    )

    # STEP 4: Return final Top K results
    return ranked_results[:top_k]

if __name__ == "__main__":

    query = "What is POL-201?"

    results = hybrid_retrieve(query, top_k=2)

    print("\nQUERY:")
    print(query)

    print("\nTOP HYBRID RESULTS:")

    for result in results:
        print("\n--------------------")
        print(f"Source: {result['chunk']['source']}")
        print(f"Chunk ID: {result['chunk']['chunk_id']}")
        print(f"Vector Rank: {result['vector_rank']}")
        print(f"BM25 Rank: {result['bm25_rank']}")
        print(f"RRF Score: {result['rrf_score']}")