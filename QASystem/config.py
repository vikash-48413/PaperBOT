"""
Configuration file for PaperBOT performance tuning
Optimized for fast 5MB file processing
"""

# Embedding Model Options (choose based on speed vs quality tradeoff)
EMBEDDING_MODELS = {
    "fast": {
        "name": "all-MiniLM-L6-v2",  # Fast: 384 dims, ~5-10x faster
        "dimension": 384,
        "description": "Fastest processing, good for large documents"
    },
    "balanced": {
        "name": "BAAI/bge-base-en-v1.5",  # Balanced: 768 dims
        "dimension": 768,
        "description": "Good balance of speed and quality"
    },
    "quality": {
        "name": "BAAI/bge-large-en-v1.5",  # Best quality: 1024 dims
        "dimension": 1024,
        "description": "Best quality, slower processing"
    }
}

# Current model selection - Keep "quality" to match existing Pinecone index (1024 dims)
# NOTE: Changing model requires recreating Pinecone index with matching dimension
CURRENT_MODEL = "quality"  # Must match Pinecone index dimension (1024)

# Document Processing Settings (Optimized for speed)
CHUNK_SETTINGS = {
    "split_by": "word",
    "split_length": 300,  # Larger chunks = fewer embeddings = faster
    "split_overlap": 15,  # Reduced overlap for speed
}

# Maximum characters per chunk (Pinecone limit is 40KB)
MAX_CHUNK_CHARS = 10000  # ~10KB max per chunk

# Batch Processing Settings - Larger batches for faster processing
BATCH_SIZE = 32  # Larger batches are faster

# Large File Optimization
LARGE_FILE_THRESHOLD = 2 * 1024 * 1024  # 2MB threshold
LARGE_FILE_CHUNK_LENGTH = 400  # Larger chunks for big files
LARGE_FILE_BATCH_SIZE = 48  # Larger batches for big files

# Auto-switch to fast model for very large files (>5MB)
AUTO_SWITCH_MODEL_FOR_LARGE_FILES = True
VERY_LARGE_FILE_THRESHOLD = 5 * 1024 * 1024  # 5MB

# Pre-warm model on startup for faster first upload
PREWARM_MODEL_ON_STARTUP = True
