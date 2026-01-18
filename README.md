# 🤖 PaperBOT - AI Research Assistant

PaperBOT is an intelligent document analysis system that uses **RAG (Retrieval Augmented Generation)** to help you understand and query research papers, documents, and data files. Upload any supported document and ask questions in natural language!

## ✨ Key Features

- 📄 **Multi-Format Support**: PDF, DOCX, DOC, TXT, MD, CSV, JSON, XLSX, XLS
- ⚡ **Parallel Processing**: Fast document ingestion with multi-threaded embedding
- 🧠 **Smart Semantic Search**: Powered by Pinecone vector database
- 💾 **Memory Management**: Optimized batch processing with automatic cleanup
- 🎯 **RAG Pipeline**: Combines retrieval with Google Gemini for accurate answers
- 🎨 **Beautiful UI**: Modern, responsive interface with drag-and-drop upload
- 🔧 **Configurable**: Choose between speed and quality modes

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Pinecone API key ([Get it here](https://www.pinecone.io/))
- Google AI API key ([Get it here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd PaperBOT
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env and add your API keys
   PINECONE_API_KEY=your_key_here
   GOOGLE_API_KEY=your_key_here
   ```

5. **Setup Pinecone Index**
   - Create index named `paperbot`
   - Dimensions: `1024`
   - Metric: `cosine`

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open in browser**
   ```
   http://localhost:8000
   ```

## 📖 Usage

1. **Upload Document**: Drag & drop or click to upload (PDF, DOCX, CSV, etc.)
2. **Wait for Processing**: Progress bar shows upload and embedding status
3. **Ask Questions**: Type your question in natural language
4. **Customize Response**: Select explanation style and length
5. **Get Answers**: AI generates context-aware answers from your document

## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI (async Python web framework)
- **Vector DB**: Pinecone (cloud-native vector database)
- **RAG Framework**: Haystack AI
- **Embeddings**: Sentence Transformers (BAAI/bge-large-en-v1.5)
- **LLM**: Google Gemini 1.5 Flash
- **Frontend**: HTML/CSS/JS with Bootstrap

### Processing Pipeline

```
Document Upload
    ↓
File Validation & Storage
    ↓
Format Detection & Conversion
    ↓
Text Extraction
    ↓
Chunking (250 words, 50 overlap)
    ↓
Parallel Batch Embedding (32 chunks/batch)
    ↓
Vector Storage (Pinecone)
    ↓
Ready for Queries!
```

### Query Pipeline

```
User Query
    ↓
Query Embedding
    ↓
Semantic Search (Top 10 chunks)
    ↓
Context Assembly
    ↓
LLM Generation (Gemini)
    ↓
Formatted Answer
```

## ⚙️ Configuration

Edit [`QASystem/config.py`](QASystem/config.py) for performance tuning:

### Fast Mode (5-10x faster)
```python
CURRENT_MODEL = "fast"
BATCH_SIZE = 64
CHUNK_SETTINGS = {
    "split_length": 400,
    "split_overlap": 50
}
```

### Quality Mode (best accuracy)
```python
CURRENT_MODEL = "quality"
BATCH_SIZE = 16
CHUNK_SETTINGS = {
    "split_length": 200,
    "split_overlap": 75
}
```

## 📊 Performance

Tested on mid-range hardware (16GB RAM, i7 CPU):

| Metric | Performance |
|--------|------------|
| Upload Speed | 1-3 seconds |
| Processing Speed | 30-50 chunks/sec |
| Query Response | 2-5 seconds |
| Memory Usage | 500MB - 2GB |

**Processing Times (typical)**:
- 10-page PDF: ~15-30 seconds
- 50-page PDF: ~60-90 seconds
- 100-page PDF: ~2-3 minutes

## 🎯 Use Cases

- 📚 **Academic Research**: Understand complex papers quickly
- 📊 **Data Analysis**: Query CSV/Excel files naturally
- 📝 **Documentation**: Search technical docs and manuals
- 💼 **Business**: Analyze reports and presentations
- 🔬 **Research**: Extract insights from scientific papers

## 🔧 Advanced Features

### Memory Management
- Automatic garbage collection every 5 batches
- Real-time memory monitoring
- Configurable batch sizes
- Resource cleanup after processing

### Semantic Search
- Vector similarity search with Pinecone
- Top-K retrieval with relevance scoring
- Namespace isolation per document
- Fallback retrieval strategies

### Error Handling
- Comprehensive validation
- Graceful API failure fallbacks
- Detailed error messages
- Automatic retry mechanisms

## 📁 Project Structure

```
PaperBOT/
├── app.py                          # FastAPI application
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup
├── .env.example                    # Environment template
├── INSTALLATION.md                 # Detailed setup guide
├── FEATURES.md                     # Feature documentation
├── QASystem/
│   ├── __init__.py
│   ├── config.py                   # Configuration settings
│   ├── ingestion.py                # Document processing
│   ├── retrieval_and_generation.py # RAG pipeline
│   └── utils.py                    # Utilities
├── templates/
│   └── index.html                  # Web interface
├── uploads/                        # Temporary file storage
└── data/                           # Sample documents
```

## 🛠️ Troubleshooting

### Out of Memory
- Reduce `BATCH_SIZE` to 8 or 16
- Use `CURRENT_MODEL = "fast"`
- Process smaller documents

### Slow Processing
- Increase `BATCH_SIZE` to 64
- Use `CURRENT_MODEL = "fast"`
- Check internet connection

### API Errors
- Verify API keys in `.env`
- Check Pinecone index configuration
- Ensure sufficient API quotas

### Upload Fails
- Check file size (max 50MB)
- Verify file format is supported
- Check console (F12) for details

## 📚 Documentation

- [Installation Guide](INSTALLATION.md) - Detailed setup instructions
- [Features](FEATURES.md) - Comprehensive feature list
- [Configuration](QASystem/config.py) - Performance tuning options

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional file format support
- More embedding model options
- Advanced retrieval strategies
- UI/UX enhancements
- Performance optimizations

## 📄 License

This project is open source. Feel free to use and modify.

## 🙏 Acknowledgments

- **Haystack AI** - RAG framework
- **Pinecone** - Vector database
- **Google AI** - Gemini LLM
- **Sentence Transformers** - Embedding models

## 📞 Support

For issues and questions:
1. Check [INSTALLATION.md](INSTALLATION.md) for setup help
2. Review [FEATURES.md](FEATURES.md) for usage details
3. Check console output for error details
4. Open an issue on GitHub

---

**Made with ❤️ for researchers, students, and knowledge workers**
