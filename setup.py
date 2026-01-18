from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="paperbot",
    version="1.0.0",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core Web Framework
        "fastapi>=0.128.0",
        "uvicorn>=0.40.0",
        "python-multipart>=0.0.21",
        "jinja2>=3.1.6",
        
        # Haystack AI Framework
        "haystack-ai>=2.22.0",
        
        # Vector Database - Pinecone
        "pinecone>=8.0.0",
        "pinecone-haystack>=6.0.0",
        
        # LLM Integration - Google Gemini
        "google-ai-haystack>=5.4.0",
        "google-generativeai>=0.8.6",
        
        # Embeddings & ML
        "sentence-transformers>=5.2.0",
        "transformers>=4.57.0",
        "torch>=2.0.0",
        
        # NLP & Text Processing
        "nltk>=3.9.0",
        
        # Document Processing
        "pypdf>=6.6.0",
        "python-docx>=1.2.0",
        "openpyxl>=3.1.5",
        "markdown>=3.10",
        
        # Data Processing
        "pandas>=2.3.0",
        "numpy>=2.0.0",
        
        # Utilities
        "python-dotenv>=1.2.0",
        "requests>=2.32.0",
        "tqdm>=4.67.0",
        "psutil>=7.2.0",
        "pydantic>=2.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "paperbot=app:main",
        ],
    },
)