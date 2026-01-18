# PaperBOT Installation Guide

## Prerequisites
- Python 3.9 or higher
- Pinecone account and API key
- Google AI (Gemini) API key

## Quick Start

### 1. Clone or Download the Repository
```bash
cd PaperBOT
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
1. Copy `.env.example` to `.env`:
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```
   PINECONE_API_KEY=your_actual_pinecone_key
   GOOGLE_API_KEY=your_actual_google_ai_key
   ```

### 5. Setup Pinecone Index
1. Log in to [Pinecone Console](https://app.pinecone.io/)
2. Create a new index with these settings:
   - **Name**: `paperbot`
   - **Dimensions**: `1024`
   - **Metric**: `cosine`
   - **Pod Type**: `Starter` or `s1`

### 6. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:8000`

## Supported File Formats
- **PDF** (.pdf)
- **Word Documents** (.docx, .doc)
- **Text Files** (.txt)
- **Markdown** (.md)
- **CSV** (.csv)
- **JSON** (.json)
- **Excel** (.xlsx, .xls)

## Performance Optimization

### For Faster Processing
Edit `QASystem/config.py`:
```python
CURRENT_MODEL = "fast"  # Use fast embedding model
BATCH_SIZE = 64         # Increase batch size
```

### For Better Quality
Edit `QASystem/config.py`:
```python
CURRENT_MODEL = "quality"  # Use high-quality model
CHUNK_SETTINGS = {
    "split_length": 200,   # Smaller chunks for precision
    "split_overlap": 75
}
```

## Troubleshooting

### Out of Memory Errors
- Reduce `BATCH_SIZE` in `config.py` to 16 or 8
- Use `CURRENT_MODEL = "fast"` for smaller memory footprint

### Slow Upload Times
- Increase `BATCH_SIZE` for parallel processing
- Use `CURRENT_MODEL = "fast"` for faster embedding

### API Rate Limits
- Wait a moment between requests
- Check your API key quotas

## System Requirements
- **RAM**: Minimum 4GB (8GB+ recommended)
- **Storage**: 2GB free space for models
- **Internet**: Required for API calls

## Need Help?
Check the console output (F12 in browser) for detailed error messages.
