# ✈️ Aerovault AI - Evaluation Report

## 1. Project Overview

Aerovault AI is an aviation-focused Retrieval Augmented Generation (RAG) assistant.

The system retrieves relevant information from aviation documents and generates grounded answers using a Large Language Model.

The main goal is to provide reliable aviation information while reducing hallucination through retrieval confidence validation.

---

# 2. Objective

The objectives of this project are:

- Build an AI assistant for aviation documents
- Implement a complete RAG pipeline
- Retrieve relevant document chunks efficiently
- Generate context-based answers
- Provide citations from source documents
- Reduce incorrect LLM responses using confidence checks

---

# 3. System Architecture

```
Aviation PDFs
      |
      v
PDF Loader
      |
      v
Text Chunking
      |
      v
Embedding Model
      |
      v
FAISS Vector Database
      |
      v
Similarity Retrieval
      |
      v
Confidence Validation
      |
      v
LLM Answer Generation
      |
      v
Answer + Confidence + Sources
```

---

# 4. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| RAG Framework | LangChain |
| Vector Database | FAISS |
| Embedding Model | Sentence Transformers |
| LLM | Gemini API |
| PDF Processing | PyPDF |

---

# 5. Dataset

The knowledge base contains aviation-related documents.

Documents include:

- Navigation
- Meteorology
- Flight Planning
- Instruments
- Aviation Regulations
- Mass and Balance

Total processed:

- 10 aviation PDF documents
- 3181 pages
- 6396 text chunks

---

# 6. RAG Pipeline Implementation

## Document Ingestion

The system:

1. Loads PDF files
2. Extracts text
3. Splits text into smaller chunks
4. Creates embeddings
5. Stores vectors in FAISS

---

## Retrieval

For every user question:

1. Query is converted into an embedding
2. FAISS performs similarity search
3. Top relevant chunks are retrieved
4. Retrieved context is passed to the LLM

---

## Generation

The LLM is instructed:

- Answer only from provided context
- Do not use external knowledge
- Refuse when information is unavailable

---

# 7. Level 2 Enhancement

## Confidence-Based Retrieval Guardrail

A confidence layer was added to improve reliability.

The system calculates confidence from retrieval similarity scores.

Confidence levels:

| Score | Label |
|---|---|
| >= 75% | High |
| 50-75% | Medium |
| < 50% | Low |

When confidence is low, the system refuses to generate unsupported answers.

---

# 8. Evaluation Test Cases

## Test Case 1

Question:

```
What is Air Traffic Service?
```

Result:

```
Confidence: 93%
Level: High
```

Status:

PASS


---

## Test Case 2

Question:

```
What is wind speed?
```

Result:

```
Confidence: 93%
Level: High
```

Status:

PASS


---

## Test Case 3

Question:

```
Who is the president of NASA?
```

Expected:

Information not available in aviation documents.

Result:

Low confidence refusal.

Status:

PASS

---

# 9. Evaluation Metrics

## Retrieval Quality

Relevant aviation chunks were successfully retrieved for domain-related queries.

Result:

Successful retrieval of aviation information.


## Grounding

Answers are generated only using retrieved document context.

Result:

Reduced hallucination.


## Citation Accuracy

The system returns:

- Document name
- Page number

for retrieved sources.

---

# 10. User Interface Evaluation

The Streamlit interface provides:

- Chat-based interaction
- Confidence indicator
- Source display
- Aviation-themed UI

---

# 11. Limitations

Current limitations:

- Requires rebuilding index after adding documents
- Depends on available aviation documents
- No authentication
- Single-user deployment

---

# 12. Future Improvements

Possible enhancements:

- PDF upload from UI
- Automatic indexing
- Hybrid retrieval (BM25 + Vector)
- Reranking
- Chat memory
- Cloud deployment
- Automated evaluation pipeline

---

# 13. Conclusion

Aerovault AI demonstrates a reliable aviation RAG system.

The project combines document retrieval, vector search, LLM generation, and confidence-based validation to provide accurate and explainable aviation answers.