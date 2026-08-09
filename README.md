# 🤖 AI Business Operations Copilot

An enterprise-grade AI system built with **RAG (Retrieval-Augmented Generation)** and a **4-agent architecture** that lets you query company documents in plain English and get accurate, context-grounded answers.

---

## 🏗️ Architecture

```
User Query
    │
    ▼
Streamlit Frontend  ──────►  FastAPI Backend
                                   │
                          Agent Orchestrator
                         ┌──────────┴─────────────┐
                     🧠 Planner         🔍 Researcher
                         │                   │
                     ⚙️ Executor ◄──── FAISS + Embeddings
                         │              (knowledge docs)
                     ✅ Reviewer
                         │
                  Final Answer + Sources + Confidence
```

### The 4 Agents

| Agent | Role |
|-------|------|
| 🧠 **Planner** | Breaks the query into 2–4 actionable steps |
| 🔍 **Researcher** | Retrieves the most relevant document chunks via FAISS |
| ⚙️ **Executor** | Sends context + query to Llama 3, generates the answer |
| ✅ **Reviewer** | Scores confidence based on how well sources support the answer |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Llama 3 (via Ollama — runs locally) |
| Embeddings | `all-MiniLM-L6-v2` (HuggingFace Sentence Transformers) |
| Vector Store | FAISS |
| Language | Python 3.11+ |

---

## 📁 Project Structure

```
AI-Business-Operations-Copilot/
├── backend/
│   ├── app/
│   │   ├── agents/          # Planner, Researcher, Executor, Reviewer, Orchestrator
│   │   ├── api/routes/      # FastAPI route handlers (chat, documents, health)
│   │   ├── config/          # App settings (Pydantic)
│   │   ├── embeddings/      # SentenceTransformer wrapper
│   │   ├── ingestion/       # Load → Chunk → Embed pipeline
│   │   ├── retriever/       # FAISS similarity search
│   │   ├── schemas/         # Pydantic request/response models
│   │   ├── services/        # Ollama LLM client
│   │   ├── vector_store/    # FAISS index management
│   │   └── main.py          # FastAPI app entry point
│   ├── knowledge/           # Your company documents (.txt files)
│   ├── faiss_index/         # Auto-generated index files (gitignored)
│   ├── .env                 # Environment variables
│   └── requirements.txt
│
└── frontend/
    ├── app.py               # Homepage
    ├── pages/               # 6 Streamlit pages
    ├── components/          # Reusable UI components
    ├── utils/               # API client, helpers, constants
    ├── assets/styles.css    # Custom dark-mode CSS
    └── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running with Llama 3:

```bash
ollama pull llama3
ollama serve
```

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend

```bash
cd backend
uvicorn app.main:app --reload
```

On first start, the system will automatically:
1. Load all `.txt` files from `backend/knowledge/`
2. Chunk them into overlapping segments
3. Generate embeddings using `all-MiniLM-L6-v2`
4. Build and save a FAISS index to `backend/faiss_index/`

Backend runs at: **http://localhost:8000**  
API docs: **http://localhost:8000/docs**

### 3. Install Frontend Dependencies

```bash
cd frontend
pip install -r requirements.txt
```

### 4. Start the Frontend

```bash
cd frontend
streamlit run app.py
```

Frontend runs at: **http://localhost:8501**

---

## 📖 Adding Your Own Documents

Drop any `.txt` file into `backend/knowledge/` and either:
- Restart the backend (auto-ingests on startup if no index exists), or
- Use the **Documents** page in the UI to upload files directly, or
- Click **Re-ingest All Documents** in the UI

---

## 🌐 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health + index status |
| `/chat/` | POST | Ask a question (runs full agent pipeline) |
| `/documents/list` | GET | List all indexed documents |
| `/documents/upload` | POST | Upload a new `.txt` document |
| `/documents/reingest` | POST | Rebuild index from all files |
| `/documents/{filename}` | DELETE | Remove a document and rebuild |

### Example Chat Request

```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the leave policy?", "top_k": 5}'
```

### Example Response

```json
{
  "answer": "Employees are entitled to 20 earned leave days per year...",
  "plan": ["Search HR policy for leave entitlements", "Identify leave types and durations"],
  "sources": [{"filename": "hr_policy.txt", "chunk": "...", "score": 0.91}],
  "confidence": 0.87,
  "timing": {"planner": 2.1, "researcher": 0.4, "executor": 8.3, "reviewer": 0.01}
}
```

---

## 📄 Sample Knowledge Base

The project includes 4 sample documents to get started:

- `company_policy.txt` — Work hours, WFH, leave, payroll, IT policy
- `hr_policy.txt` — Recruitment, performance, benefits, exit policy
- `sop_customer_support.txt` — Ticket SLAs, escalation procedures, templates
- `financial_report_q1_2024.txt` — Revenue, expenses, KPIs, customer metrics
