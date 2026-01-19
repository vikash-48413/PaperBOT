import os
from dotenv import load_dotenv
from haystack_integrations.document_stores.pinecone import PineconeDocumentStore
from haystack.utils import Secret

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Import config to get current model dimension
try:
    from QASystem.config import CURRENT_MODEL, EMBEDDING_MODELS
    MODEL_DIMENSION = EMBEDDING_MODELS[CURRENT_MODEL]["dimension"]
except ImportError:
    MODEL_DIMENSION = 384  # Default to fast model dimension

# Validate required environment variables
MISSING_VARS = []
if not PINECONE_API_KEY:
    MISSING_VARS.append("PINECONE_API_KEY")
    print("⚠️  WARNING: PINECONE_API_KEY not set! Document storage will fail.")
else:
    os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
    print("✅ Pinecone API key set successfully.")

if not GOOGLE_API_KEY:
    MISSING_VARS.append("GOOGLE_API_KEY")
    print("⚠️  WARNING: GOOGLE_API_KEY not set! AI responses will fail.")
else:
    os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
    print("✅ Google API key set successfully.")

if HF_TOKEN:
    os.environ['HF_TOKEN'] = HF_TOKEN
    print("✅ HF_TOKEN set successfully.")
else:
    print("ℹ️  INFO: HF_TOKEN not set (optional for most models)")

if MISSING_VARS:
    print(f"\n⚠️  CRITICAL: Missing required environment variables: {', '.join(MISSING_VARS)}")
    print("   For Hugging Face Spaces: Set these as 'Secrets' in Space Settings")
    print("   For local development: Create a .env file with these values\n")

print(f"Using embedding dimension: {MODEL_DIMENSION}")

def pinecone_config(namespace="default"):
    """
    Configure Pinecone database with namespace isolation.
    Using a single namespace ensures only one document is active at a time.
    """
    if not PINECONE_API_KEY:
        raise ValueError(
            "PINECONE_API_KEY is not set! "
            "For HF Spaces: Add it as a Secret in Space Settings. "
            "For local: Add it to your .env file."
        )
    
    document_store = PineconeDocumentStore(
        api_key=Secret.from_token(PINECONE_API_KEY),
        index="paperbot",
        namespace=namespace,  # Use namespace to isolate documents
        dimension=MODEL_DIMENSION,  # Dynamic dimension based on selected model
        metric="cosine"
    )
    return document_store