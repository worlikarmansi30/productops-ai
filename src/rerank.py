import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from hybrid_retrieve import hybrid_retrieve


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score_relevance(query, chunk_text):

    prompt = f"""
You are evaluating whether a retrieved document chunk is relevant
to a user's question.

QUESTION:
{query}

DOCUMENT CHUNK:
{chunk_text}

Rate how relevant this chunk is for answering the question.

Use a score from 0 to 10:

0 = completely irrelevant
5 = somewhat relevant
10 = directly answers the question

Return ONLY a JSON object in this format:

{{"score": 0}}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    result = json.loads(response.output_text)

    return result["score"]

def rerank_results(query, results, top_k=2):

    reranked_results = []

    for result in results:

        chunk = result["chunk"]

        score = score_relevance(
            query,
            chunk["text"]
        )

        reranked_results.append({
            "chunk": chunk,
            "rerank_score": score,
            "rrf_score": result["rrf_score"],
            "vector_rank": result["vector_rank"],
            "bm25_rank": result["bm25_rank"]
        })

    # Higher reranker score = better
    reranked_results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_results[:top_k]

if __name__ == "__main__":

    query = "What causes payment failures?"

    # Get candidate chunks from hybrid retrieval
    hybrid_results = hybrid_retrieve(query, top_k=5)

    # Rerank those candidates and keep the best 2
    results = rerank_results(
        query,
        hybrid_results,
        top_k=2
    )

    print("\nQUERY:")
    print(query)

    print("\nTOP RERANKED RESULTS:")

    for result in results:
        print("\n--------------------")
        print(f"Source: {result['chunk']['source']}")
        print(f"Chunk ID: {result['chunk']['chunk_id']}")
        print(f"Vector Rank: {result['vector_rank']}")
        print(f"BM25 Rank: {result['bm25_rank']}")
        print(f"RRF Score: {result['rrf_score']}")
        print(f"Rerank Score: {result['rerank_score']}")