from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="paperbot",
    version="2.1.0",
    author="Vikash",
    author_email="vikash17052005@gmail.com",
    description="AI-Powered Research Paper Assistant with RAG using Haystack, Pinecone, and Google Gemini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vikash-48413/PaperBOT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        # Core Web Framework
        "fastapi>=0.115.0",
        "uvicorn>=0.30.0",
        "python-multipart>=0.0.9",
        "jinja2>=3.1.4",
        
        # Haystack AI Framework
        "haystack-ai>=2.4.0",
        
        # Vector Database - Pinecone
        "pinecone-haystack>=2.0.0",
        
        # LLM Integration - Google Gemini
        "google-ai-haystack>=2.0.0",
        
        # Embeddings
        "sentence-transformers>=3.0.0",
        
        # Document Processing
        "pypdf>=4.0.0",
        "python-docx>=1.1.0",
        "openpyxl>=3.1.0",
        "markdown>=3.5.0",
        "pandas>=2.1.0",
        
        # Utilities
        "python-dotenv>=1.0.0",
        "psutil>=5.9.0",
        "tqdm>=4.66.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)
