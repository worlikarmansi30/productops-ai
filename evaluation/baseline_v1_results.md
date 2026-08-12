# Baseline RAG v1 — Evaluation Results

## Version
Baseline RAG v1

## Retrieval Architecture
- OpenAI embeddings
- ChromaDB vector database
- Vector similarity search
- Top-K retrieval: 2
- Maximum distance threshold: 1.2
- No BM25
- No reranking

## Knowledge Base
Documents: 3

- checkout_prd.md
- returns_policy.md
- payments_prd.md

Total indexed chunks: 7

## Evaluation Dataset
Total questions: 7

- Answerable questions: 5
- Unanswerable questions: 2

## Results

| Metric | Result |
|---|---:|
| Correct Behavior | 7/7 |
| Answerability Accuracy | 100.00% |
| Answer Correctness | 100.00% |
| Retrieval Accuracy | 100.00% |
| Hit@2 | 100.00% |

## Reliability Features
- Grounded generation using retrieved context
- Source and chunk citations
- Retrieval distance threshold
- Abstention when relevant context is unavailable
- "I don't know based on the provided documents" fallback

## Notes

This is the baseline vector-only RAG implementation.

These results are based on a small 7-question evaluation dataset and should not be interpreted as production-level accuracy.

Future versions will use a larger and more challenging evaluation dataset.

## Next Version

Baseline RAG v1 will be compared against:

Hybrid RAG v2
- Vector search
- BM25 keyword retrieval
- Result fusion
- Reranking