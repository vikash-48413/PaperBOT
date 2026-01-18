"""Test Pinecone connection and configuration"""
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

try:
    print("🔍 Testing Pinecone connection...")
    api_key = os.getenv("PINECONE_API_KEY")
    print(f"   API Key: {api_key[:10]}...{api_key[-5:]}")
    
    pc = Pinecone(api_key=api_key)
    print("   ✅ Pinecone client initialized")
    
    # List indexes
    indexes = pc.list_indexes()
    print(f"\n📊 Available indexes:")
    for idx in indexes:
        print(f"   • {idx}")
    
    # Check if paperbot index exists
    index_name = "paperbot"
    if any(idx.name == index_name for idx in indexes):
        print(f"\n✅ Index '{index_name}' exists")
        
        # Get index info
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        print(f"\n📈 Index stats:")
        print(f"   • Dimension: {stats.get('dimension', 'N/A')}")
        print(f"   • Total vectors: {stats.get('total_vector_count', 0)}")
        print(f"   • Namespaces: {list(stats.get('namespaces', {}).keys())}")
        
        # Check namespace
        namespaces = stats.get('namespaces', {})
        if 'current_document' in namespaces:
            ns_stats = namespaces['current_document']
            print(f"\n📁 Namespace 'current_document':")
            print(f"   • Vector count: {ns_stats.get('vector_count', 0)}")
    else:
        print(f"\n❌ Index '{index_name}' NOT found!")
        print("   You need to create this index in Pinecone console")
        print("   Dimension: 1024, Metric: cosine")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
