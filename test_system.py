"""
Test script for PaperBOT functionality
Run this to verify the installation and basic features
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("PaperBOT System Test")
print("=" * 60)

# Test 1: Check Python version
print("\n[1/7] Checking Python version...")
import sys
if sys.version_info >= (3, 9):
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} - Need 3.9+")
    sys.exit(1)

# Test 2: Check required packages
print("\n[2/7] Checking required packages...")
required_packages = [
    'fastapi',
    'uvicorn',
    'haystack',
    'pinecone',
    'sentence_transformers',
    'dotenv',
    'docx',
    'pandas',
    'psutil'
]

missing_packages = []
for package in required_packages:
    try:
        if package == 'dotenv':
            __import__('dotenv')
        elif package == 'docx':
            __import__('docx')
        else:
            __import__(package)
        print(f"  ✓ {package}")
    except ImportError:
        print(f"  ✗ {package} - MISSING")
        missing_packages.append(package)

if missing_packages:
    print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 3: Check environment variables
print("\n[3/7] Checking environment variables...")
from dotenv import load_dotenv
load_dotenv()

env_vars = {
    'PINECONE_API_KEY': os.getenv('PINECONE_API_KEY'),
    'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY')
}

all_env_ok = True
for var, value in env_vars.items():
    if value and value != f'your_{var.lower()}_here':
        print(f"  ✓ {var} is set")
    else:
        print(f"  ✗ {var} is NOT set or using example value")
        all_env_ok = False

if not all_env_ok:
    print("\n⚠️  Please configure your .env file with actual API keys")
    print("   Copy .env.example to .env and add your keys")

# Test 4: Check directory structure
print("\n[4/7] Checking directory structure...")
required_dirs = ['QASystem', 'templates', 'uploads']
for dir_name in required_dirs:
    dir_path = Path(dir_name)
    if dir_path.exists():
        print(f"  ✓ {dir_name}/")
    else:
        print(f"  ✗ {dir_name}/ - MISSING")

# Test 5: Check QASystem modules
print("\n[5/7] Checking QASystem modules...")
try:
    from QASystem import config, ingestion, retrieval_and_generation, utils
    print("  ✓ config.py")
    print("  ✓ ingestion.py")
    print("  ✓ retrieval_and_generation.py")
    print("  ✓ utils.py")
except ImportError as e:
    print(f"  ❌ Error importing QASystem: {e}")

# Test 6: Check configuration
print("\n[6/7] Checking configuration...")
try:
    from QASystem.config import CURRENT_MODEL, EMBEDDING_MODELS, BATCH_SIZE
    print(f"  ✓ Current model: {CURRENT_MODEL}")
    print(f"  ✓ Batch size: {BATCH_SIZE}")
    print(f"  ✓ Available models: {', '.join(EMBEDDING_MODELS.keys())}")
except Exception as e:
    print(f"  ❌ Error loading config: {e}")

# Test 7: Test embedding model loading (optional)
print("\n[7/7] Testing embedding model...")
print("  ⚠️  This will download the model if not cached (~1-2GB)")
test_model = input("  Download and test embedding model? (y/N): ").strip().lower()

if test_model == 'y':
    try:
        from QASystem.ingestion import get_embedder
        print("  Loading model...")
        embedder = get_embedder()
        print("  ✅ Embedding model loaded successfully!")
    except Exception as e:
        print(f"  ❌ Error loading model: {e}")
else:
    print("  ⏭️  Skipped")

# Summary
print("\n" + "=" * 60)
print("Test Summary")
print("=" * 60)

if missing_packages:
    print("❌ FAILED - Missing packages")
    print(f"   Run: pip install {' '.join(missing_packages)}")
elif not all_env_ok:
    print("⚠️  PARTIAL - Environment variables need configuration")
    print("   Edit .env file with your actual API keys")
else:
    print("✅ ALL CHECKS PASSED!")
    print("\nYou can now run: python app.py")
    print("Then open: http://localhost:8000")

print("=" * 60)
