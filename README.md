# 🧠 RAG-Based Question Answering System

---

## 📖 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system for question answering.

It enhances large language models by integrating **external knowledge retrieval**, improving factual accuracy and reducing hallucinations.

---

## 🔄 System Workflow

### 📌 Pipeline Overview

```text id="flow_001"
User Question
   ↓
Agent Task Understanding
   ↓
RAG Pipeline
   ├── Hybrid Search (BM25 + Embedding Retrieval)
   ├── Reranking (Relevance Optimization)
   └── Context Construction
   ↓
Prompt Construction
   ↓
LLM Generation
   ↓
Final Answer

