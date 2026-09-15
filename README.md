# Enterprise AI Compliance & Contract Risk Agent

An AI-powered contract analysis application that uses **Retrieval-Augmented Generation (RAG), semantic search, and a local Large Language Model (LLM)** to identify potential contractual compliance and operational risks.

The application analyzes contract documents and produces **structured risk findings, supporting evidence, contract page references, severity levels, recommendations, compliance checks, and an overall risk score.**

> **Note:** The contract included in this repository is fully synthetic and contains intentionally introduced risk scenarios for testing and evaluation. No confidential company or client information is used.

---

## 🎯 Why I Built This

This project was built to gain practical hands-on experience with **Generative AI, RAG pipelines, semantic search, LLM integration, and AI-based risk analysis**, while connecting these technologies with my previous experience in **Risk & Compliance, Python, SQL, and automation**.

The goal was to build a practical AI application rather than a simple chatbot.

The system focuses on a realistic enterprise use case:

**Can an AI system analyze a contract, retrieve the relevant evidence, identify potential contractual risks, and generate an explainable risk report?**

---

## 💡 What the Application Does

A user provides a contract PDF.

The system then:

1. Extracts text while preserving page numbers.
2. Splits the document into overlapping chunks.
3. Converts each chunk into an embedding vector.
4. Stores the processed content in a local knowledge base.
5. Converts the user's analysis request into an embedding.
6. Retrieves the most relevant contract sections using semantic similarity.
7. Sends only the retrieved evidence to the local Qwen3 LLM.
8. Extracts structured contractual risk findings.
9. Normalizes risk categories.
10. Assigns severity and numerical risk scores.
11. Runs deterministic compliance checks.
12. Generates a professional contract risk report.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │     Contract PDF    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌──────────────
```
