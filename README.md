<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.128+-00a393?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Haystack-2.22+-1C3D5A?style=for-the-badge" alt="Haystack">
  <img src="https://img.shields.io/badge/Pinecone-Vector_DB-6b21a8?style=for-the-badge" alt="Pinecone">
  <img src="https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<h1 align="center">🤖 PaperBOT</h1>
<h3 align="center">AI-Powered Research Paper Assistant</h3>

<p align="center">
  <b>Upload any document and ask questions in natural language. Get AI-powered answers grounded in your document's content.</b>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-usage">Usage</a> •
  <a href="#%EF%B8%8F-configuration">Configuration</a> •
  <a href="#-api-reference">API</a> •
  <a href="#-architecture">Architecture</a>
</p>

---

## 🎯 What is PaperBOT?

PaperBOT is a **Retrieval-Augmented Generation (RAG)** application that allows you to upload research papers, documents, or data files and have intelligent conversations about their content. Unlike generic chatbots, PaperBOT answers are **always grounded in your uploaded document**, preventing hallucinations and ensuring accuracy.

### Key Highlights

- 📄 **Multi-format Support** — PDF, DOCX, TXT, MD, CSV, JSON, Excel
- 🚀 **Fast Processing** — Parallel embedding with optimized chunking
- 🎯 **Accurate Answers** — RAG ensures responses come from your document
- 🎨 **Beautiful UI** — Modern, responsive interface with progress tracking
- 🔒 **Privacy First** — Your documents stay on your infrastructure

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📚 Document Processing
- **9 file formats** supported
- Smart text chunking (300 words/chunk)
- Parallel batch embedding
- Metadata size enforcement for Pinecone

</td>
<td width="50%">

### 🧠 AI-Powered Q&A
- Semantic search with Pinecone
- Google Gemini 2.0 Flash for generation
- Curated fallback responses
- Customizable response styles

</td>
</tr>
<tr>
<td width="50%">

### ⚡ Performance
- Model pre-warming on startup
- Configurable speed/quality tradeoff
- Memory-efficient processing
- Up to 15MB file support

</td>
<td width="50%">

### 🎨 User Experience
- Drag-and-drop file upload
- Real-time progress tracking
- In-browser document preview
- Preloaded files support

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.9+ | Runtime |
| Pinecone Account | Free tier | Vector database |
| Google AI API Key | Free tier | LLM generation |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/vikash-48413/PaperBOT.git
cd PaperBOT

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys (see Configuration section)

# 5. Run the application
python app.py
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

---

## 📖 Usage

### Basic Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Upload Document │ ──▶ │  Ask Questions  │ ──▶ │   Get Answers   │
│  (PDF, DOCX...) │     │  (Natural Lang) │     │  (AI-Powered)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Step-by-Step

1. **Upload a Document**
   - Drag & drop or click to select a file
   - Supported: PDF, DOCX, DOC, TXT, MD, CSV, JSON, XLSX, XLS
   - Maximum size: 15MB (recommended: under 5MB for fast processing)

2. **Wait for Processing**
   - Progress bar shows upload and embedding status
   - Processing time: ~30s for 1MB, ~2-3min for 5MB

3. **Ask Questions**
   - Type your question in natural language
   - Example: "What is the main contribution of this paper?"

4. **Customize Response**
   - **Style**: Simple, Balanced, or Technical
   - **Length**: Short, Medium, or Comprehensive

5. **Preview Document**
   - Click the 👁️ Preview button to view documents in-browser
   - No download required

### Using Preloaded Files

Place documents in the `data/` folder to make them available as preloaded options:

```bash
# Add a paper to preloaded files
cp your-paper.pdf data/
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required: Pinecone Vector Database
PINECONE_API_KEY=your_pinecone_api_key_here

# Required: Google AI (Gemini)
GOOGLE_API_KEY=your_google_api_key_here

# Optional: HuggingFace (for some models)
HF_TOKEN=your_huggingface_token_here
```

### Getting API Keys

| Service | Link | Notes |
|---------|------|-------|
| Pinecone | [pinecone.io](https://www.pinecone.io/) | Free tier: 1 index, 100K vectors |
| Google AI | [aistudio.google.com](https://aistudio.google.com/) | Free tier: 60 requests/min |
| HuggingFace | [huggingface.co](https://huggingface.co/) | Optional, for gated models |

### Pinecone Index Setup

Create an index with these settings:

| Setting | Value |
|---------|-------|
| **Name** | `paperbot` |
| **Dimensions** | `1024` |
| **Metric** | `cosine` |
| **Cloud** | Any (AWS, GCP, Azure) |

### Performance Tuning

Edit `QASystem/config.py` to adjust:

```python
# Embedding model (must match Pinecone dimensions)
CURRENT_MODEL = "quality"  # Options: "fast", "balanced", "quality"

# Chunk settings
CHUNK_SETTINGS = {
    "split_by": "word",
    "split_length": 300,    # Words per chunk
    "split_overlap": 15,    # Overlap between chunks
}

# Batch size for embeddings
BATCH_SIZE = 32  # Higher = faster, but uses more memory
```

---

## 📡 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main web interface |
| `POST` | `/upload_document` | Upload and process a document |
| `POST` | `/get_result` | Ask a question |
| `GET` | `/document_status` | Check current document status |
| `GET` | `/preview_document` | Preview current document |
| `GET` | `/preview_file/{filename}` | Preview any file |
| `POST` | `/delete_document` | Delete current document |
| `GET` | `/preloaded_files` | List preloaded files |
| `POST` | `/load_preloaded_file` | Load a preloaded file |
| `GET` | `/model_status` | Check if embedding model is ready |

### Example: Ask a Question (cURL)

```bash
curl -X POST "http://localhost:8000/get_result" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "question=What is attention mechanism?&style=Balanced&length=Medium"
```

### Response Format

```json
{
  "answer": "The attention mechanism allows the model to focus on relevant parts of the input...",
  "source_file": "attention_paper.pdf"
}
```

---

## 🏗️ Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                           PaperBOT                                │
├──────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────────┐  │
│  │   FastAPI   │───▶│  Haystack    │───▶│  Google Gemini      │  │
│  │   Server    │    │  Pipeline    │    │  (LLM Generation)   │  │
│  └─────────────┘    └──────────────┘    └─────────────────────┘  │
│         │                  │                                      │
│         ▼                  ▼                                      │
│  ┌─────────────┐    ┌──────────────┐                             │
│  │  Document   │    │   Pinecone   │                             │
│  │  Converters │    │  Vector DB   │                             │
│  └─────────────┘    └──────────────┘                             │
└──────────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI + Uvicorn | Async web server |
| **RAG Framework** | Haystack 2.22 | Pipeline orchestration |
| **Embeddings** | Sentence Transformers | BAAI/bge-large-en-v1.5 |
| **Vector DB** | Pinecone | Semantic search |
| **LLM** | Google Gemini 2.0 Flash | Answer generation |
| **Frontend** | HTML/CSS/JS + Bootstrap | User interface |

### Processing Pipeline

```
Document Upload
      │
      ▼
┌─────────────────┐
│ File Validation │  ← Check type, size
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Format Converter│  ← PDF, DOCX, Excel → Text
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Text Chunking   │  ← 300 words/chunk
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Size Enforcement│  ← Ensure <8KB per chunk
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Batch Embedding │  ← 32 chunks/batch
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pinecone Upload │  ← Store vectors
└─────────────────┘
```

---

## 📁 Project Structure

```
PaperBOT/
├── app.py                 # Main FastAPI application
├── QASystem/              # Core RAG system
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── ingestion.py       # Document processing & embedding
│   ├── retrieval_and_generation.py  # Q&A pipeline
│   └── utils.py           # Pinecone utilities
├── templates/             # HTML templates
│   └── index.html         # Main UI
├── data/                  # Preloaded documents
├── uploads/               # User uploads (gitignored)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── start.bat              # Windows launcher
├── start.sh               # Linux/Mac launcher
└── LICENSE                # MIT License
```

---

## 🧪 Testing

### Run System Tests

```bash
# Test all components
python test_system.py

# Test Pinecone connection
python test_pinecone.py
```

### Manual Testing Checklist

1. **Upload Test**: Upload a small PDF (<1MB)
2. **Query Test**: Ask "What is this document about?"
3. **Preview Test**: Click the preview button
4. **Delete Test**: Delete the document

---

## 🔧 Troubleshooting

### Common Issues

<details>
<summary><b>❌ "Pinecone index not found"</b></summary>

Create the index in Pinecone console:
- Name: `paperbot`
- Dimensions: `1024`
- Metric: `cosine`
</details>

<details>
<summary><b>❌ "Google API quota exceeded"</b></summary>

The free tier has rate limits. Either:
- Wait a few minutes for quota reset
- Upgrade to paid tier
- Use curated fallback (automatic)
</details>

<details>
<summary><b>❌ "File too large" error</b></summary>

Maximum file size is 15MB. For faster processing:
- Keep files under 5MB
- Split large documents into chapters
</details>

<details>
<summary><b>❌ Server not starting</b></summary>

1. Check if port 8000 is in use
2. Verify virtual environment is activated
3. Check all dependencies: `pip install -r requirements.txt`
</details>

<details>
<summary><b>❌ "Model dimension mismatch"</b></summary>

The embedding model dimension must match Pinecone index:
- `fast` model → 384 dimensions
- `balanced` model → 768 dimensions
- `quality` model → 1024 dimensions

Either recreate the Pinecone index or change `CURRENT_MODEL` in config.py
</details>

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black . --line-length 100
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Vikash**
- GitHub: [@vikash-48413](https://github.com/vikash-48413)
- Email: vikash17052005@gmail.com

---

## 🙏 Acknowledgments

- [Haystack](https://haystack.deepset.ai/) — RAG framework
- [Pinecone](https://www.pinecone.io/) — Vector database
- [Google AI](https://ai.google.dev/) — Gemini LLM
- [Sentence Transformers](https://www.sbert.net/) — Embeddings
- [FastAPI](https://fastapi.tiangolo.com/) — Web framework

---

<p align="center">
  <b>⭐ Star this repository if you find it useful!</b>
</p>
