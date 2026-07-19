# Multi-Agent AI Research Assistant

Upload documents, chat with them using retrieval-augmented generation (RAG), and generate research reports as PDFs — all running locally.

## Features

- **Document Upload** — Upload documents to be parsed, chunked, and embedded for retrieval.
- **Chat with Documents** — Ask questions and get answers grounded in your uploaded content, with source citations.
- **Report Generation** — Provide a title and research question; the assistant retrieves relevant context and generates a structured PDF report.

## Tech Stack

**Backend**
- FastAPI (REST API)
- LangChain + LangGraph (agent/RAG orchestration)
- Groq (`llama-3.3-70b-versatile`) via `langchain-groq` (LLM inference)
- ChromaDB (vector store)
- `sentence-transformers` (`all-MiniLM-L6-v2`) for embeddings
- SQLAlchemy + SQLite (chat history / metadata)
- `fpdf2` (PDF report generation)

**Frontend**
- Streamlit

## Project Structure

```
my-ai-research-assistant/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI routes
│   │   ├── core/           # config, database, logging
│   │   ├── prompts/        # prompt templates
│   │   ├── rag/            # retriever agent
│   │   ├── repositories/   # DB access layer
│   │   └── services/       # chat, document, report, LLM services
│   ├── data/                # generated reports, SQLite DB (gitignored)
│   ├── uploads/              # uploaded documents (gitignored)
│   ├── vector_db/            # ChromaDB persistence (gitignored)
│   ├── tests/
│   └── requirements.txt
└── README.md
```

## Setup

### 1. Clone and enter the project
```bash
cd my-ai-research-assistant/backend
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file inside `backend/`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the backend
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 6. Run the frontend
```bash
streamlit run <your_streamlit_app_file>.py
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/documents/upload` | Upload one or more documents |
| POST | `/api/chat` | Ask a question about uploaded documents |
| POST | `/api/reports/generate` | Generate a PDF research report |

## Status

- ✅ Document upload
- ✅ RAG-based chat with citations
- ✅ PDF report generation
- ⬜ DOCX report export
- ⬜ Deployment (currently local-only)

## Notes

- Uses SQLite for local persistence; not suited for multi-instance deployment as-is.
- `sentence-transformers` pulls in PyTorch as a dependency — be mindful of build size limits on free-tier hosting platforms if deploying.
