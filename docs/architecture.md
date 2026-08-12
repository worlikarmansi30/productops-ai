# ProductOps AI — System Architecture

## Overview

ProductOps AI is a Retrieval-Augmented Generation (RAG) application that allows users to ask natural-language questions across product requirements and policy documents.

The final prototype uses Hybrid Retrieval combining semantic vector search and BM25 keyword search.

## Architecture

User
  ↓
Streamlit Interface
  ↓
User Question
  ↓
┌─────────────────────────────┐
│      Hybrid Retrieval       │
│                             │
│  Vector Search     BM25     │
│  (ChromaDB)      Search     │
│       ↓             ↓       │
│       └──────┬──────┘       │
│              ↓              │
│     Reciprocal Rank Fusion  │
└──────────────┬──────────────┘
               ↓
        Top Relevant Chunks
               ↓
        Context Assembly
               ↓
              LLM
               ↓
       Grounded Response
               ↓
      Answer + Source Citation

## Knowledge Base

The prototype knowledge base contains three documents:

- Checkout Product Requirements Document
- Payment Processing Product Requirements Document
- Returns Policy

Documents are split into chunks and stored as embeddings in ChromaDB.

## Retrieval

### Vector Retrieval

Semantic embeddings retrieve chunks based on conceptual similarity between the user query and document content.

### BM25 Retrieval

BM25 provides lexical keyword matching and improves retrieval of exact terms and document identifiers such as `POL-201`.

### Reciprocal Rank Fusion

Results from vector retrieval and BM25 are combined using Reciprocal Rank Fusion (RRF).

This allows the system to benefit from both semantic similarity and exact keyword matching.

## Generation

The highest-ranked chunks are provided to the language model as context.

The model is instructed to answer only from the retrieved documentation.

Responses include source document and chunk citations.

## Hallucination Guardrail

When sufficient supporting information is not available in the retrieved documents, the system responds:

"I don't know based on the provided documents."

This prevents the application from intentionally answering unsupported questions.

## Architecture Decision

Three architectures were evaluated:

1. Vector-only RAG — V1
2. Hybrid Vector + BM25 + RRF — V2
3. Hybrid Retrieval + LLM Reranking — V3

Hybrid V2 was selected for the final prototype because it improved retrieval performance over V1 while avoiding the additional LLM inference required by V3.

## Evaluation

On the expanded retrieval benchmark:

| Metric | Vector V1 | Hybrid V2 |
|---|---:|---:|
| Top-1 Source Accuracy | 86.96% | 91.30% |
| Hit@2 | 86.96% | 95.65% |

The evaluation dataset contained 30 questions, including 23 answerable questions and 7 unsupported questions.

## Application Layer

The final system is exposed through a Streamlit interface where users can:

- Enter natural-language questions
- Receive grounded answers
- View source citations
- Receive an abstention response for unsupported questions