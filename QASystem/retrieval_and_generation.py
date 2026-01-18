from haystack.utils import Secret
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.retrievers.pinecone import PineconeEmbeddingRetriever
from haystack_integrations.components.generators.google_ai import GoogleAIGeminiGenerator
from haystack import Pipeline
from haystack.components.rankers import TransformersSimilarityRanker
from QASystem.utils import pinecone_config
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
import time
import re

# Load environment variables
load_dotenv()

# Import config to get current model
try:
    from QASystem.config import CURRENT_MODEL, EMBEDDING_MODELS
    RETRIEVAL_MODEL = EMBEDDING_MODELS[CURRENT_MODEL]["name"]
    print(f"Using retrieval model: {RETRIEVAL_MODEL}")
except ImportError:
    RETRIEVAL_MODEL = "all-MiniLM-L6-v2"  # Fast model as default
    print(f"Using default retrieval model: {RETRIEVAL_MODEL}")

# ============================================================================
# OUTPUT CURATION FUNCTIONS
# ============================================================================

def clean_retrieved_text(text: str) -> str:
    """Clean and format retrieved text for better readability."""
    # Remove excessive whitespace while preserving paragraph breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # Clean up common PDF artifacts
    text = re.sub(r'(\d+)\s*\n\s*(\d+)', r'\1\2', text)  # Join split numbers
    text = re.sub(r'-\s*\n\s*', '', text)  # Join hyphenated words
    
    # Format mathematical notations for markdown
    text = re.sub(r'\^(\d+)', r'<sup>\1</sup>', text)  # Superscripts
    text = re.sub(r'_(\d+)', r'<sub>\1</sub>', text)  # Subscripts
    
    return text.strip()

def extract_key_concepts(text: str, query: str) -> List[str]:
    """Extract key concepts from text that relate to the query."""
    # Common ML/AI terms to look for
    ml_terms = [
        'attention', 'transformer', 'encoder', 'decoder', 'embedding',
        'softmax', 'layer', 'neural', 'model', 'training', 'query',
        'key', 'value', 'matrix', 'vector', 'dimension', 'head',
        'multi-head', 'self-attention', 'feed-forward', 'positional'
    ]
    
    query_lower = query.lower()
    text_lower = text.lower()
    
    found_concepts = []
    for term in ml_terms:
        if term in query_lower or term in text_lower:
            found_concepts.append(term)
    
    return found_concepts[:5]  # Return top 5 concepts

def format_curated_response(docs: list, query: str, style: str = "Balanced", length: str = "Medium") -> str:
    """
    Create a well-curated response from retrieved documents when AI generation fails.
    This provides a structured, readable fallback that maintains document integrity.
    """
    if not docs:
        return "❌ **No relevant information found**\n\nThe uploaded document does not contain information about your question."
    
    # Sort by relevance score
    sorted_docs = sorted(docs, key=lambda x: x.score if x.score else 0, reverse=True)
    
    # Build curated response
    response_parts = []
    
    # Header with query context
    response_parts.append(f"## 📚 Research Findings: {query}\n")
    
    # Extract key concepts
    all_text = " ".join([d.content for d in sorted_docs[:3]])
    concepts = extract_key_concepts(all_text, query)
    if concepts:
        concept_tags = " • ".join([f"`{c}`" for c in concepts])
        response_parts.append(f"**Key Concepts:** {concept_tags}\n")
    
    response_parts.append("---\n")
    
    # Determine how many sections to show based on length preference
    if "short" in length.lower():
        max_sections = 1
        max_chars = 800
    elif "comprehensive" in length.lower() or "long" in length.lower():
        max_sections = 4
        max_chars = 2500
    else:  # Medium
        max_sections = 2
        max_chars = 1500
    
    # Process each relevant section
    total_chars = 0
    for i, doc in enumerate(sorted_docs[:max_sections], 1):
        if total_chars >= max_chars:
            break
            
        content = clean_retrieved_text(doc.content)
        
        # Calculate relevance percentage
        relevance = doc.score * 100 if doc.score else 0
        relevance_emoji = "🟢" if relevance >= 75 else "🟡" if relevance >= 50 else "🟠"
        
        # Section header
        response_parts.append(f"### {relevance_emoji} Section {i} — Relevance: {relevance:.0f}%\n")
        
        # Truncate if needed for this section
        section_limit = max_chars - total_chars
        if len(content) > section_limit:
            content = content[:section_limit] + "..."
        
        response_parts.append(f"{content}\n")
        total_chars += len(content)
    
    # Add source metadata
    response_parts.append("\n---")
    response_parts.append(f"\n📊 **Retrieved {len(sorted_docs)} relevant sections** from your document")
    
    # Get source file if available
    if sorted_docs[0].meta and sorted_docs[0].meta.get('source'):
        source = sorted_docs[0].meta.get('source', 'Unknown')
        response_parts.append(f"\n📄 **Source:** {source}")
    
    # Add note about fallback
    response_parts.append("\n\n> ℹ️ *This response shows direct excerpts from the paper. AI-powered summarization is temporarily unavailable due to API rate limits.*")
    
    return "\n".join(response_parts)

prompt_template = """You are an expert AI research assistant helping users understand academic papers. Provide clear, well-structured answers based ONLY on the provided context.

📄 **Context from the research paper:**
{% for doc in documents %}
---
{{ doc.content }}
---
{% endfor %}

❓ **Question:** {{query}}

🎨 **Style:** {{style}} | 📏 **Length:** {{length}}

## Response Guidelines:

### ✅ DO:
- Answer ONLY using information from the context above
- Quote or reference specific parts when relevant
- Use markdown formatting (headers, bullets, code blocks)
- Include mathematical formulas if present in context (use LaTeX: $formula$)
- Structure response with clear sections

### ❌ DON'T:
- Use external knowledge not in the context
- Make assumptions beyond what's stated
- Fabricate information

### If information is missing:
State: "This specific information is not available in the provided paper sections."

---

**Your well-structured answer:**"""
 
def get_result(query: str, style: str = "Balanced", length: str = "Medium (2-3 paragraphs)") -> str:
    """
    Get answer from the RAG pipeline with enhanced semantic search and retrieval.
    Creates fresh pipeline components for each query to avoid sharing issues.
    
    Features:
    - Retry logic for rate limits
    - Curated fallback responses
    - Proper error handling
    
    Args:
        query: The user's question
        style: Explanation style (e.g., "Simple and Intuitive", "Detailed and Technical", "Balanced")
        length: Response length (e.g., "Short (1 paragraph)", "Medium (2-3 paragraphs)", "Comprehensive")
    
    Returns:
        Formatted answer string with metadata
    """
    start_time = time.time()
    max_retries = 3
    retry_delay = 8  # seconds
    
    try:
        print(f"\n[QUERY] Processing: '{query[:50]}...'")
        
        # Step 1: Always retrieve documents first (this doesn't have rate limits)
        print("   [INFO] Retrieving relevant documents...")
        
        retrieval_pipeline = Pipeline()
        text_embedder = SentenceTransformersTextEmbedder(model=RETRIEVAL_MODEL)
        retriever = PineconeEmbeddingRetriever(
            document_store=pinecone_config(namespace="default"), 
            top_k=10  # Retrieve more candidates for better coverage
        )
        
        retrieval_pipeline.add_component("text_embedder", text_embedder)
        retrieval_pipeline.add_component("retriever", retriever)
        retrieval_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        
        retrieval_results = retrieval_pipeline.run({"text_embedder": {"text": query}})
        retrieved_docs = retrieval_results['retriever']['documents']
        
        if not retrieved_docs:
            return "❌ **No relevant information found**\n\nThe uploaded document does not appear to contain information about your question. Please try:\n- Rephrasing your question\n- Uploading a document that covers this topic"
        
        doc_count = len(retrieved_docs)
        avg_score = sum([doc.score for doc in retrieved_docs if doc.score]) / max(doc_count, 1)
        print(f"   [OK] Retrieved {doc_count} chunks (avg relevance: {avg_score:.3f})")
        
        # Step 2: Try AI generation with retry logic
        for attempt in range(max_retries):
            try:
                print(f"   [INFO] Generating AI response (attempt {attempt + 1}/{max_retries})...")
                
                # Create generation pipeline
                gen_pipeline = Pipeline()
                
                prompt_builder = PromptBuilder(
                    template=prompt_template, 
                    required_variables=["query", "documents", "style", "length"]
                )
                
                # Use Gemini with optimized settings
                llm = GoogleAIGeminiGenerator(
                    api_key=Secret.from_env_var("GOOGLE_API_KEY"),
                    model="gemini-2.0-flash",
                    generation_config={
                        "max_output_tokens": 2000,
                        "temperature": 0.7,
                        "top_p": 0.95
                    }
                )
                
                gen_pipeline.add_component("prompt_builder", prompt_builder)
                gen_pipeline.add_component("llm", llm)
                gen_pipeline.connect("prompt_builder.prompt", "llm")
                
                # Run generation with pre-retrieved documents
                gen_results = gen_pipeline.run({
                    "prompt_builder": {
                        "query": query, 
                        "documents": retrieved_docs[:5],  # Use top 5 for context
                        "style": style, 
                        "length": length
                    }
                })
                
                answer = gen_results['llm']['replies'][0]
                
                elapsed_time = time.time() - start_time
                print(f"   [OK] AI response generated in {elapsed_time:.2f}s")
                
                # Add metadata footer
                footer = f"\n\n---\n✅ *AI-generated from {doc_count} relevant sections (relevance: {avg_score:.0%}) in {elapsed_time:.1f}s*"
                
                return answer + footer
                
            except Exception as gen_error:
                error_str = str(gen_error)
                
                # Check if it's a rate limit error
                if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)
                        print(f"   [WARN] Rate limited. Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"   [WARN] Rate limit persists. Using curated fallback.")
                        break
                else:
                    print(f"   [ERROR] Generation failed: {error_str}")
                    break
        
        # Step 3: Curated fallback response (no AI needed)
        print("   [INFO] Generating curated fallback response...")
        curated_response = format_curated_response(retrieved_docs, query, style, length)
        
        elapsed_time = time.time() - start_time
        print(f"   [OK] Curated response ready in {elapsed_time:.2f}s")
        
        return curated_response
        
    except Exception as e:
        print(f"   [ERROR] Critical error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return f"""❌ **Error Processing Your Question**

We encountered an error while processing your request.

**Error Details:** {str(e)}

**Suggestions:**
1. Ensure your document was uploaded successfully
2. Try rephrasing your question
3. Check your internet connection
4. If the problem persists, restart the server

---
*If you see rate limit errors, please wait a few minutes before trying again.*"""


if __name__ == '__main__':
    # Test the retrieval and generation
    result = get_result("What is Multi-Head Attention?")
    print(result)