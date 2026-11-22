# QueryPilot: An Agentic Multi-Strategy RAG Assistant

> A production-inspired Retrieval-Augmented Generation (RAG) system designed for JEE preparation reasoning, focusing on retrieval quality, explainability, and evaluation rather than simply generating answers.

---

## Overview

AdaptiveRAG is an advanced Retrieval-Augmented Generation (RAG) system built to answer questions from pre-indexed JEE preparation material with high accuracy and transparency.

Unlike conventional RAG chatbots that rely solely on vector search, AdaptiveRAG experiments with multiple retrieval strategies, evaluates their effectiveness, and provides complete visibility into how an answer is generated.

The project is designed as an engineering showcase demonstrating modern GenAI system design using FastAPI, LangGraph, LangChain, ChromaDB, and advanced retrieval techniques.

---

## Motivation

Most RAG implementations follow a straightforward pipeline:

```
Question
    ↓
Vector Search
    ↓
LLM
    ↓
Answer
```

While simple, this approach often suffers from:

* Poor retrieval for keyword-heavy queries
* Missing relevant context
* Hallucinated responses
* No explainability
* No evaluation framework

AdaptiveRAG addresses these shortcomings by introducing a modular retrieval pipeline that combines traditional information retrieval with semantic search and modern reranking techniques.

---

# Goals

The primary objectives of this project are:

* Build a modular and extensible retrieval engine.
* Improve retrieval quality using hybrid search techniques.
* Minimize hallucinations through better context selection.
* Provide explainability for every generated response.
* Benchmark multiple retrieval strategies.
* Demonstrate production-inspired GenAI architecture.

---

# Dataset

The system operates on a pre-indexed corpus consisting of:

* NCERT Physics, Chemistry, and Mathematics (Class 11–12)
* JEE coaching notes and study modules
* Official JEE Main previous year papers
* Official JEE Advanced previous year papers
* NTA JEE Main and JEE Advanced syllabus

The corpus is indexed offline before serving user queries.

---

# High-Level Architecture

```
                    React Frontend
                           │
                    FastAPI Backend
                           │
                     Chat Service
                           │
                  LangGraph Workflow
                           │
                 Retrieval Engine
                           │
    ┌───────────┬────────────┬──────────────┐
    │           │            │
  BM25      Vector Search   Web Search
    │           │
    └────── Hybrid Retrieval ──────┘
                   │
        Reciprocal Rank Fusion
                   │
         Cross Encoder Reranker
                   │
       Contextual Compression
                   │
             Citation Builder
                   │
                 LLM
                   │
              Final Response
```

---

# Retrieval Pipeline

Every query passes through the following stages:

1. Intent Detection
2. Query Rewriting
3. Hybrid Retrieval
4. Reciprocal Rank Fusion
5. Cross-Encoder Reranking
6. Contextual Compression
7. Prompt Construction
8. Response Generation
9. Citation Verification

Each stage is independently testable and replaceable.

---

# Explainability

AdaptiveRAG exposes the retrieval process behind every answer.

Users can inspect:

* Original Query
* Rewritten Query
* BM25 Results
* Vector Search Results
* Hybrid Retrieval Output
* Reranked Chunks
* Compressed Context
* Final Prompt
* Source Citations

This makes the system easier to debug and significantly improves trust in generated responses.

---

# Evaluation

Instead of evaluating only the final answer, AdaptiveRAG benchmarks the retrieval pipeline itself.

Metrics include:

* Precision@k
* Recall@k
* Mean Reciprocal Rank (MRR)
* Context Precision
* Context Recall
* Answer Relevancy
* Faithfulness
* Latency
* Token Usage

These benchmarks help quantify the impact of different retrieval strategies.

---

# Technology Stack

## Backend

* Python
* FastAPI
* LangChain
* LangGraph
* PostgreSQL

## Retrieval

* ChromaDB
* BM25
* Reciprocal Rank Fusion
* Cross-Encoder Reranker
* Contextual Compression

## Frontend

* React
* TypeScript
* Axios

## LLM

* OpenAI GPT Models

---

# Project Structure

```
adaptive-rag/

backend/
    app/
        api/
        config/
        retrieval/
        graph/
        services/
        tools/
        evaluation/
        prompts/
        database/
        utils/

frontend/

data/

docs/

tests/
```

---

# Planned Features

* Advanced Hybrid Retrieval
* Query Rewriting
* Reciprocal Rank Fusion
* Cross-Encoder Reranking
* Contextual Compression
* Tool Calling
* Explainability Mode
* Retrieval Benchmarks
* Source Citations
* LangSmith Tracing

---

# Future Work

* Adaptive retrieval strategies based on query intent.
* GraphRAG integration.
* Domain-specific fine-tuned embeddings.
* Multi-modal document support.
* Offline evaluation dashboard.
* Multi-model benchmarking.

---

# License

This project is intended for educational and research purposes.

Commercial use of copyrighted study material should comply with the respective publishers' licensing terms.
