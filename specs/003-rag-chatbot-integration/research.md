# Research Summary: RAG Chatbot Integration for Docusaurus Textbook

## Decision: Tech Stack Selection
**Rationale**: Based on the constitution requirements, we must use the specified tech stack: Docusaurus (frontend), FastAPI (backend), Qdrant (vector DB), OpenAI Agents SDK with Gemini API (AI layer), ChatKit SDK (chat handling), and Neon Postgres (metadata/session storage).

**Alternatives considered**:
- Using different vector databases (Pinecone, Weaviate, Chroma) - rejected in favor of Qdrant per constitution
- Using different backend frameworks (Express, Django) - rejected in favor of FastAPI per constitution
- Using different AI providers (OpenAI, Anthropic) - constitution specifies OpenAI Agents SDK with Gemini API

## Decision: Frontend Integration Approach
**Rationale**: The chatbot UI must be seamlessly integrated into the existing Docusaurus website as specified in the constitution's User Experience and Interactivity principle.

**Implementation**: Use Docusaurus' ability to inject custom React components via swizzling or MDX components to embed the chat interface on textbook pages.

## Decision: Textbook Content Processing
**Rationale**: To ensure the chatbot only uses textbook content (per constitution's Accuracy and Content Fidelity principle), we need to process all textbook markdown files into a vector database.

**Implementation**: Parse all /docs/*.md files from the Docusaurus site, chunk them into semantic segments, and store embeddings in Qdrant for retrieval.

## Decision: Semantic Search Implementation
**Rationale**: The constitution requires semantic search priority using vector embeddings for meaning-based retrieval over keyword matching.

**Implementation**: Use embedding models to convert both textbook content and user queries to vectors, then perform similarity search in Qdrant.

## Decision: Response Generation Constraints
**Rationale**: Constitution requires no external knowledge, hallucinations, or internet sources - responses must be grounded in textbook content only.

**Implementation**: Use RAG (Retrieval-Augmented Generation) approach where the LLM only receives textbook content as context for response generation.

## Decision: Session Management
**Rationale**: Constitution requires maintaining conversational context across exchanges.

**Implementation**: Store conversation history in Neon Postgres with session IDs linked to user interactions.

## Decision: Text Selection Feature
**Rationale**: Constitution supports text selection for targeted queries as specified in the feature requirements.

**Implementation**: Add JavaScript to detect text selection on textbook pages and pass the selected text as context to the chat API.