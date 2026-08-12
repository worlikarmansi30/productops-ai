# Hybrid RAG v2 — Evaluation Results

## Architecture

Hybrid retrieval using:

- Vector semantic search
- ChromaDB
- BM25 keyword search
- Reciprocal Rank Fusion (RRF)
- Top-K retrieval
- Grounded LLM generation
- Source citations
- Abstention for unsupported questions

## Knowledge Base

Documents: 3

- checkout_prd.md
- returns_policy.md
- payments_prd.md

Total indexed chunks: 7

## Evaluation Dataset

Total questions: 8

- Answerable questions: 6
- Unanswerable questions: 2

## Results

| Metric | Baseline v1 | Hybrid v2 |
|---|---:|---:|
| Answerability Accuracy | 87.50% | 100.00% |
| Answer Correctness | 83.33% | 100.00% |
| Correct Answers | 5/6 | 6/6 |

## Key Finding

Hybrid retrieval successfully answered the exact-identifier query:

"What is POL-201?"

Baseline vector retrieval failed to retrieve sufficiently relevant context for this query.

BM25 matched the exact identifier, allowing Hybrid RAG v2 to retrieve the Returns Policy and generate the correct grounded answer.

## Improvement

Answerability Accuracy:
87.50% → 100.00%

Answer Correctness:
83.33% → 100.00%

## Reliability Improvement

Hybrid v2 was also configured so unsupported questions return:

"I don't know based on the provided documents."

without attaching unsupported source citations.

## Limitation

The current evaluation dataset contains only 8 questions across 3 documents.

These results demonstrate the behavior of the prototype but should not be interpreted as production-level accuracy.

A larger and more challenging evaluation benchmark will be required.