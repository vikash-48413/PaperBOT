import os
from dotenv import load_dotenv
from haystack_integrations.document_stores.pinecone import PineconeDocumentStore
from haystack.utils import Secret

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Import config to get current model dimension
try:
    from QASystem.config import CURRENT_MODEL, EMBEDDING_MODELS
    MODEL_DIMENSION = EMBEDDING_MODELS[CURRENT_MODEL]["dimension"]
except ImportError:
    MODEL_DIMENSION = 384  # Default to fast model dimension

# setting env variable
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
os.environ['HF_TOKEN'] = HF_TOKEN

print("Pinecone API key set successfully.")
print(f"Using embedding dimension: {MODEL_DIMENSION}")

def pinecone_config(namespace="default"):
    """
    Configure Pinecone database with namespace isolation.
    Using a single namespace ensures only one document is active at a time.
    """
    document_store = PineconeDocumentStore(
        api_key=Secret.from_token(PINECONE_API_KEY),
        index="paperbot",
        namespace=namespace,  # Use namespace to isolate documents
        dimension=MODEL_DIMENSION,  # Dynamic dimension based on selected model
        metric="cosine"
    )
    return document_store