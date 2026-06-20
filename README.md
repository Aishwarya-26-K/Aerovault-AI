# ✈️ Aviation RAG Assistant

An AI-powered aviation document assistant built using **Retrieval Augmented Generation (RAG)**.

The system answers aviation-related questions by retrieving information from aviation PDFs and generating grounded responses using an LLM.

---

## 🚀 Features

- 📄 PDF document ingestion
- ✂️ Intelligent text chunking
- 🧠 Sentence Transformer embeddings
- 🔎 FAISS vector similarity search
- 🤖 LLM-powered answer generation
- 🛡️ Confidence-based hallucination prevention
- 📌 Source document and page tracking
- 💬 Streamlit chat interface
- ✈️ Aviation-focused knowledge base

---

## 🏗️ System Architecture

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
            FAISS Vector Store
                     |
                     v
              Retriever
                     |
                     v
          Confidence Validation
                     |
                     v
              LLM Generator
                     |
                     v
       Answer + Confidence + Sources
```

---

## 📂 Project Structure

```
Aviation_RAG_Assistant/

│
├── app/
│   ├── api/              # FastAPI routes
│   ├── embeddings/       # Embedding generation
│   ├── ingestion/        # PDF loading & chunking
│   ├── llm/              # LLM integration
│   ├── rag/              # RAG pipeline
│   ├── retrieval/        # Similarity search
│   ├── vectorstore/      # FAISS management
│   └── main.py
│
├── ui/
│   └── chat.py           # Streamlit UI
│
├── scripts/
│   └── build_index.py    # Build FAISS index
│
├── documents/            # Aviation PDFs
│
└── README.md
```

---

## 🛠️ Tech Stack

- Python
- FastAPI
- LangChain
- FAISS
- Sentence Transformers
- Streamlit
- Gemini API

---

## ▶️ How to Run

### 1. Activate environment

```
.\.venv\Scripts\activate
```

### 2. Build vector index

```
python scripts/build_index.py
```

### 3. Start backend

```
uvicorn app.main:app --reload
```

### 4. Start UI

```
streamlit run ui/chat.py
```

---

## 🔍 Example

Question:

```
What is Air Traffic Service?
```

Response:

```
Air Traffic Services are services provided to aircraft including:
- Flight Information Service
- Alerting Service
- Air Traffic Control Service

Confidence: High

Sources:
Instruments.pdf - Page 325
```

---

## 🎯 Project Goal

To create a reliable aviation assistant that provides accurate answers from trusted aviation documents while reducing LLM hallucination using retrieval confidence checks.