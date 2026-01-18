# PaperBOT Quick Reference

## 🚀 Quick Commands

### First Time Setup
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate (Windows)
venv\Scripts\activate

# 2. Activate (Linux/Mac)
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run application
python app.py
```

### Daily Usage
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

## 📝 API Keys Setup

### Pinecone
1. Go to https://www.pinecone.io/
2. Sign up/Login
3. Create new API key
4. Copy to `.env` file

### Google AI (Gemini)
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Copy to `.env` file

### Pinecone Index Setup
1. Login to Pinecone Console
2. Click "Create Index"
3. Settings:
   - Name: `paperbot`
   - Dimensions: `1024`
   - Metric: `cosine`
   - Cloud: Any (AWS/GCP/Azure)
   - Region: Choose nearest

## ⚙️ Configuration Options

### Speed vs Quality (`QASystem/config.py`)

**Fast Mode** (Recommended for large docs):
```python
CURRENT_MODEL = "fast"
BATCH_SIZE = 64
```

**Quality Mode** (Recommended for technical papers):
```python
CURRENT_MODEL = "quality"
BATCH_SIZE = 16
```

## 🎯 Supported File Types

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | .pdf | Best for research papers |
| Word | .docx, .doc | Full text extraction |
| Text | .txt | Plain text |
| Markdown | .md | Preserves formatting |
| CSV | .csv | Tabular data |
| Excel | .xlsx, .xls | Spreadsheets |
| JSON | .json | Structured data |

## 🔧 Troubleshooting

### Issue: Out of Memory
**Solution**: Reduce batch size in `config.py`
```python
BATCH_SIZE = 8  # Lower value
```

### Issue: Slow Upload
**Solution**: Use fast model
```python
CURRENT_MODEL = "fast"
```

### Issue: API Rate Limit
**Solution**: Wait 1-2 minutes between uploads

### Issue: Can't Connect to Server
**Solution**: Check if port 8000 is free
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

## 📊 Performance Tips

### For Large Documents (100+ pages)
```python
# config.py
CURRENT_MODEL = "fast"
BATCH_SIZE = 64
CHUNK_SETTINGS = {
    "split_length": 400,
    "split_overlap": 50
}
```

### For Technical Papers
```python
# config.py
CURRENT_MODEL = "quality"
BATCH_SIZE = 16
CHUNK_SETTINGS = {
    "split_length": 200,
    "split_overlap": 75
}
```

### For CSV/Excel Files
- Keep files under 10,000 rows for best performance
- Remove unnecessary columns before upload
- Use CSV format for faster processing

## 🎨 UI Features

### Response Styles
- **Simple & Intuitive**: Easy explanations
- **Balanced**: Mix of detail and clarity
- **Detailed & Technical**: In-depth analysis
- **Academic**: Formal writing

### Response Lengths
- **Short**: 1 paragraph
- **Medium**: 2-3 paragraphs (recommended)
- **Comprehensive**: Detailed multi-paragraph

## 🔍 Example Questions

### For Research Papers
- "What is the main contribution of this paper?"
- "Explain the methodology used"
- "What are the key findings?"
- "How does this compare to previous work?"

### For Data Files (CSV/Excel)
- "What are the main trends in this data?"
- "Summarize the statistics"
- "What columns are available?"

### For Documentation
- "How do I install this software?"
- "Explain the configuration options"
- "What are the prerequisites?"

## 📈 Monitoring

### Memory Usage
Check console output for memory stats:
```
📊 Statistics:
• Memory: 1250.5MB
• Processing speed: 45 chunks/sec
```

### Performance Metrics
- Upload: 1-3 seconds
- Processing: 30-50 chunks/sec
- Query: 2-5 seconds

## 🆘 Getting Help

1. Check console output (terminal)
2. Open browser console (F12)
3. Review error messages
4. Check [INSTALLATION.md](INSTALLATION.md)
5. Review [FEATURES.md](FEATURES.md)

## 🔄 Updates & Maintenance

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Clear Cache
```bash
# Delete uploads
rm -rf uploads/*

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Reset Database
Delete all vectors in Pinecone console or via code

## 🎓 Best Practices

1. **One Document at a Time**: Upload new doc clears previous
2. **Appropriate Model**: Use fast for speed, quality for accuracy
3. **Clear Questions**: Be specific in your queries
4. **File Size**: Keep under 50MB for best performance
5. **Internet**: Stable connection required for API calls

---

**Need more help?** Check the full documentation in [README.md](README.md)
