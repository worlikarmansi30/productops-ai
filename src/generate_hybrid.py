import os

from dotenv import load_dotenv
from openai import OpenAI

from hybrid_retrieve import hybrid_retrieve

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_hybrid_answer(query):

    # STEP 1: Retrieve context using hybrid retrieval
    results = hybrid_retrieve(query, top_k=2)

    # If no relevant context was found, stop here
    if not results:
        return "I don't know based on the provided documents."

    # STEP 2: Build context for the LLM
    context_parts = []

    for result in results:
        chunk = result["chunk"]

        context_parts.append(
            f"""
Source: {chunk['source']}
Chunk ID: {chunk['chunk_id']}
Content:
{chunk['text']}
"""
        )

    context = "\n".join(context_parts)

    # STEP 3: Create grounded prompt
    prompt = f"""
You are a product knowledge assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be supported by the context, say:
"I don't know based on the provided documents."

Do not use outside knowledge.
Do not invent information.

If the answer is supported by the context, cite the supporting source
at the end using this format:

Source: filename, Chunk ID: number

If the answer is NOT supported by the context, respond exactly:

I don't know based on the provided documents.

Do NOT include a source citation when you do not know the answer.

CONTEXT:
{context}

QUESTION:
{query}
"""

    # STEP 4: Generate answer
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

if __name__ == "__main__":

    query = input("Ask a question: ")

    answer = generate_hybrid_answer(query)

    print("\nFINAL ANSWER:")
    print(answer)