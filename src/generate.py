from openai import OpenAI
from dotenv import load_dotenv
import os

from retrieve import retrieve


# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(query):

    # STEP 1: Retrieve relevant chunks from ChromaDB
    results = retrieve(query, top_k=2)
    
        # If no relevant chunks were found, stop here
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

    # STEP 3: Ask the LLM to answer using only retrieved context
    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions="""
You are a product knowledge assistant.

Answer the user's question using ONLY the provided context.

If the answer is not explicitly supported by the context, say exactly:

I don't know based on the provided documents.

Do not use outside knowledge.
Do not guess or make up information.

If you can answer the question, provide a concise answer.

At the end, cite the supporting source using this format:

Source: filename, Chunk ID: number
""",
        input=f"""
CONTEXT:

{context}


QUESTION:

{query}
"""
    )

    return response.output_text


if __name__ == "__main__":

    query = input("Ask a question: ")

    answer = generate_answer(query)

    print("\nFINAL ANSWER:")
    print(answer)