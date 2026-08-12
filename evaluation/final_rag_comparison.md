# RAG Architecture Comparison

## Objective

Compare the performance of three RAG architectures developed during the project:

1. Baseline V1 — Vector Retrieval
2. Hybrid V2 — Vector + BM25 + Reciprocal Rank Fusion
3. Reranked V3 — Hybrid Retrieval + LLM Reranking

---

## Architecture Evolution

### Baseline V1

Vector semantic retrieval using embeddings and ChromaDB.

Pipeline:

Question → Vector Search → Top-K Chunks → LLM → Answer

### Hybrid V2

Combined semantic and lexical retrieval.

Pipeline:

Question → Vector Search + BM25 → RRF Fusion → Top-K Chunks → LLM → Answer

### Reranked V3

Added an LLM relevance-ranking stage after hybrid retrieval.

Pipeline:

Question → Vector + BM25 → RRF → Candidate Pool → LLM Reranker → Best Chunks → LLM → Answer

---

## Retrieval Evaluation

Expanded benchmark:

- 30 total questions
- 23 answerable questions
- 7 unsupported questions

| Metric | Baseline V1 | Hybrid V2 |
|---|---:|---:|
| Top-1 Source Accuracy | 86.96% | 91.30% |
| Hit@2 | 86.96% | 95.65% |

### Retrieval Improvement

Hybrid V2 improved:

- Top-1 Source Accuracy by 4.34 percentage points
- Hit@2 by 8.69 percentage points

A key improvement occurred for exact identifier queries such as:

"What is POL-201?"

Vector-only retrieval failed, while BM25 enabled Hybrid V2 to retrieve the correct policy document.

---

## Generation Evaluation

The initial generation benchmark contained:

- 8 total questions
- 6 answerable questions
- 2 unsupported questions

| Metric | Baseline V1 | Hybrid V2 | Reranked V3 |
|---|---:|---:|---:|
| Answerability Accuracy | 87.50% | 100.00% | 100.00% |
| Answer Correctness | 83.33% | 100.00% | 100.00% |

Note: Generation results are based on the smaller 8-question benchmark and should not be interpreted as results from the expanded 30-question retrieval benchmark.

---

## Reranking Finding

Reranking successfully prioritized highly relevant chunks during qualitative testing.

For example, for:

"What causes payment failures?"

the reranker assigned the directly answering chunk a relevance score of 10/10.

However, Reranked V3 did not improve answerability or answer correctness over Hybrid V2 on the initial generation benchmark.

V3 also requires additional LLM inference calls, increasing system complexity, latency, and cost.

---

## Recommended Architecture

Hybrid V2 is the preferred architecture for the current prototype.

It provides:

- Better retrieval coverage than vector-only search
- Strong handling of semantic queries
- Improved handling of exact identifiers through BM25
- Lower complexity than the reranked architecture
- Fewer LLM calls than V3

Reranking remains a potential future enhancement if a larger production evaluation demonstrates sufficient quality improvement to justify the additional inference cost.

---

## Known Limitations

The system still has retrieval weaknesses.

For example:

- "What team owns PRD-205?" retrieved the correct document at rank 2 rather than rank 1.
- "Which team owns POL-201?" failed to retrieve the correct source within the top 2.

The current knowledge base also contains only three documents, so results should be interpreted as prototype-level evidence rather than production performance.

---

## Product Decision

The project demonstrates an iterative AI product development approach:

Baseline → Measure → Identify Failure → Improve Retrieval → Measure Again → Evaluate Complexity → Select Architecture

Rather than selecting the most technically complex architecture, the final recommendation is based on measurable quality improvement and implementation trade-offs.