# ProductOps AI

## AI-Powered Product Knowledge Assistant

ProductOps AI is a production-style Retrieval-Augmented Generation (RAG) application designed to help product teams quickly find reliable answers across product requirements, payment documentation, and customer policies.

Instead of manually searching through multiple documents, users can ask questions in natural language and receive grounded answers with source citations.

The project demonstrates an iterative AI product development approach: establish a baseline, measure retrieval quality, identify failure modes, improve the retrieval architecture, and evaluate whether the additional complexity creates measurable value.

### Key Capabilities

- Multi-document knowledge retrieval
- Semantic vector search
- Hybrid retrieval using Vector Search + BM25
- Reciprocal Rank Fusion (RRF)
- Source citations
- Hallucination guardrails
- "I don't know" behavior for unsupported questions
- Retrieval evaluation using Hit@2 and Top-1 Source Accuracy
- Streamlit-based user interface

## Business Problem

Product teams work across many sources of information, including product requirement documents, policies, operational documentation, and internal knowledge bases.

Finding a specific answer often requires manually searching across multiple documents. Traditional keyword search can also struggle when users phrase questions differently from the terminology used in the source document.

This creates three key challenges:

- Time spent searching across fragmented documentation
- Difficulty retrieving information when queries and documents use different wording
- Risk of AI-generated answers that are not grounded in approved documentation

## Product Goal

The goal of ProductOps AI is to provide a simple natural-language interface that allows product teams to retrieve trustworthy information from internal product documentation.

The system was designed around three product requirements:

1. **Retrieval Quality** — Surface the correct source document and relevant context.
2. **Grounded Answers** — Generate answers based only on retrieved documentation.
3. **Trust & Transparency** — Cite the source and abstain when the knowledge base does not contain sufficient information.

Rather than optimizing for model complexity, the project focuses on measurable improvements in retrieval quality and user trust.

## Solution Architecture

ProductOps AI uses a Retrieval-Augmented Generation (RAG) architecture that separates information retrieval from answer generation.

### End-to-End Flow

```text
Product Documents
       ↓
Document Ingestion
       ↓
Text Chunking
       ↓
Embeddings
       ↓
ChromaDB Vector Store
       ↓
User Question
       ↓
┌───────────────────────────────┐
│       Hybrid Retrieval        │
│                               │
│  Vector Search     BM25       │
│       ↓              ↓        │
│       └──────┬───────┘        │
│              ↓                │
│   Reciprocal Rank Fusion      │
└──────────────┬────────────────┘
               ↓
       Relevant Chunks
               ↓
        Context Assembly
               ↓
              LLM
               ↓
       Grounded Answer
               ↓
      Source Citation

## Iterative RAG Development

Rather than starting with a complex architecture, ProductOps AI was developed iteratively. Each version addressed an observed retrieval limitation and was evaluated before additional complexity was introduced.

### V1 — Vector Retrieval Baseline

The first version used semantic vector retrieval with ChromaDB.

This established the baseline RAG pipeline:

**Question → Vector Retrieval → Relevant Chunks → LLM → Grounded Answer**

V1 performed well on semantic questions but showed a limitation with exact identifiers. For example, the query:

> "What is POL-201?"

failed to retrieve the correct Returns Policy document.

This demonstrated that semantic similarity alone was not always sufficient for queries containing exact document IDs or keywords.

### V2 — Hybrid Retrieval

To address this failure mode, BM25 keyword retrieval was added alongside vector search.

The two ranked result sets were combined using Reciprocal Rank Fusion (RRF):

**Vector Search + BM25 → RRF → Ranked Context**

This improved retrieval of exact identifiers while preserving semantic retrieval performance.

On the expanded evaluation set, Hybrid V2 improved:

- **Hit@2:** 86.96% → 95.65%
- **Top-1 Source Accuracy:** 86.96% → 91.30%

### V3 — LLM Reranking

A third version introduced an LLM-based reranking step after hybrid retrieval.

The reranker evaluated candidate chunks and reordered them based on their relevance to the user's question.

V3 achieved strong answer-generation results in the initial evaluation, including:

- **Answerability Accuracy:** 100%
- **Answer Correctness:** 6/6 (100%)

However, the additional LLM call increased architecture complexity, latency, and inference cost.

### Final Architecture Decision

Hybrid V2 was selected as the final application architecture.

The decision was based on the trade-off between retrieval quality and system complexity:

| Version | Approach | Key Outcome |
|---|---|---|
| V1 | Vector Search | Strong semantic baseline but weaker exact-ID retrieval |
| V2 | Vector + BM25 + RRF | Improved retrieval with limited additional complexity |
| V3 | Hybrid + LLM Reranking | Strong results but additional latency, cost, and complexity |

The final decision followed a product principle:

> **Add AI complexity only when the measurable improvement justifies the additional cost and operational overhead.**

For this prototype, Hybrid V2 provided the strongest balance of retrieval performance, explainability, cost, and implementation simplicity.

## Evaluation

Evaluation was treated as a core part of the product development process rather than relying on individual demo questions.

### Evaluation Dataset

The expanded evaluation set contains **30 questions**, including:

- 23 answerable questions
- 7 unsupported questions
- Semantic queries
- Exact keyword and document-ID queries
- Paraphrased user questions
- Questions requiring the system to abstain

### Retrieval Metrics

Two retrieval metrics were used:

**Hit@2**

Measures whether the correct source document appears within the top two retrieved results.

**Top-1 Source Accuracy**

Measures whether the highest-ranked retrieval result comes from the correct source document.

### Final Retrieval Results

| Metric | Vector V1 | Hybrid V2 | Improvement |
|---|---:|---:|---:|
| Hit@2 | 86.96% | 95.65% | +8.69 pp |
| Top-1 Source Accuracy | 86.96% | 91.30% | +4.34 pp |

Hybrid retrieval improved both metrics over the vector-only baseline.

### Key Failure Mode Identified

One of the clearest baseline failures occurred with exact document identifiers.

For example:

> **Question:** What is POL-201?

Vector V1 failed to retrieve the Returns Policy, while Hybrid V2 successfully retrieved it.

This helped identify a limitation of semantic-only retrieval: exact identifiers may not have enough semantic meaning for embedding similarity alone.

Adding BM25 provided a complementary lexical retrieval signal.

### Hallucination / Abstention Testing

The evaluation set also included questions whose answers were intentionally absent from the knowledge base, such as:

> Who is the CEO of NovaTech?

The expected behavior was not to generate a plausible answer, but to respond:

> "I don't know based on the provided documents."

This behavior was validated through both the evaluation pipeline and the final Streamlit application.

### Evaluation Takeaway

The evaluation demonstrated that improving retrieval architecture produced measurable gains without requiring a more expensive generation model.

The result informed the decision to deploy Hybrid V2 as the final prototype architecture.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| LLM | OpenAI API |
| Embeddings | OpenAI Embeddings |
| Vector Database | ChromaDB |
| Semantic Retrieval | Vector Similarity Search |
| Keyword Retrieval | BM25 |
| Rank Fusion | Reciprocal Rank Fusion (RRF) |
| Reranking Experiment | LLM-based Reranking |
| User Interface | Streamlit |
| Evaluation | Custom Python Evaluation Framework |

## Project Structure

```text
productops-ai/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── documents/
│       ├── checkout_prd.md
│       ├── payments_prd.md
│       └── returns_policy.md
│
├── docs/
│   └── architecture.md
│
├── evaluation/
│   ├── eval_questions.json
│   ├── evaluate.py
│   ├── evaluate_retrieval.py
│   ├── compare_versions.py
│   └── evaluation results
│
├── src/
│   ├── ingest.py
│   ├── chunk.py
│   ├── embed.py
│   ├── vector_store.py
│   ├── retrieve.py
│   ├── bm25_retrieve.py
│   ├── hybrid_retrieve.py
│   ├── rerank.py
│   ├── generate.py
│   ├── generate_hybrid.py
│   └── generate_reranked.py
│
└── tests/
```

## Running the Application Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd productops-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the OpenAI API key

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
```

The `.env` file is excluded from version control and should never be committed to GitHub.

### 6. Run the application

```bash
python -m streamlit run app.py
```

Then open the local Streamlit URL displayed in the terminal.

## AI Product Manager Case Study

### Problem

Product teams often need to search across multiple PRDs, policies, and operational documents to answer relatively simple questions.

Traditional keyword search can miss semantically related information, while generative AI systems can create trust issues if answers are not grounded in approved documentation.

### Product Hypothesis

A Retrieval-Augmented Generation system combining semantic and lexical retrieval could provide faster access to internal product knowledge while maintaining transparency through citations and abstention behavior.

### MVP

The initial MVP focused on a narrow knowledge base and four core user capabilities:

1. Ask natural-language questions
2. Retrieve relevant internal documentation
3. Generate grounded answers
4. Cite the supporting source

A hallucination guardrail was added so the system could abstain when the answer was not supported by the knowledge base.

### Experimentation

The retrieval architecture was improved iteratively.

**V1 — Vector Retrieval**

Established the semantic-search baseline.

**Observed limitation:** exact identifiers such as `POL-201` could fail retrieval.

**V2 — Hybrid Retrieval**

Added BM25 and Reciprocal Rank Fusion to combine lexical and semantic retrieval.

**Result:** Hit@2 improved from **86.96% to 95.65%**, while Top-1 Source Accuracy improved from **86.96% to 91.30%**.

**V3 — LLM Reranking**

Tested whether an additional relevance-scoring step could further improve the system.

Although reranking produced strong results, it introduced another LLM inference step and therefore additional latency, cost, and architectural complexity.

### Product Decision

Hybrid V2 was selected for the final application.

The decision was not based on choosing the most technically complex architecture. It was based on selecting the architecture that provided the strongest balance between:

- Retrieval quality
- User trust
- Latency
- API cost
- Explainability
- Implementation complexity

### Product Metrics

The prototype evaluates two categories of AI product quality:

**Retrieval Quality**
- Hit@2
- Top-1 Source Accuracy

**Answer Quality**
- Answerability Accuracy
- Answer Correctness
- Appropriate abstention for unsupported questions

### Key Product Learnings

**1. Retrieval quality can matter as much as model quality.**

A strong language model cannot generate a grounded answer if the correct context is never retrieved.

**2. Semantic search and keyword search solve different problems.**

Vector retrieval performs well for conceptual similarity, while BM25 provides value for exact terminology and identifiers.

**3. Evaluation should drive architecture decisions.**

The move from V1 to V2 was based on an observed retrieval failure and measurable improvement rather than adding technology for its own sake.

**4. Abstention is a product feature.**

For enterprise knowledge applications, saying "I don't know" when evidence is unavailable can be more valuable than generating a plausible but unsupported answer.

**5. More sophisticated AI is not automatically a better product.**

V3 demonstrated the potential value of reranking, but the additional inference cost and complexity were not justified for the scope and performance of this prototype.

## Future Improvements

Potential next steps for a production deployment include:

- Larger and more diverse document collections
- Metadata-based filtering
- Role-based access controls
- Automated ingestion and document updates
- Retrieval and generation latency monitoring
- Cost-per-query monitoring
- User feedback collection
- Larger evaluation datasets
- Production observability and quality monitoring

## Project Status

**Prototype Complete**

The project demonstrates the complete lifecycle of an AI product experiment:

**Problem Definition → MVP → Baseline → Evaluation → Failure Analysis → Retrieval Improvement → Architecture Trade-off → User Interface → Final Product Decision**