# Research Document: Embedding Pipeline Implementation

## Decision: Text Extraction Method
**Rationale**: Using BeautifulSoup4 for HTML parsing to extract clean text content while preserving document structure
**Alternatives considered**:
- Selenium (for dynamic content) - rejected due to complexity for static Docusaurus sites
- Regular expressions - rejected due to fragility with complex HTML
- Scrapy - rejected due to over-engineering for simple crawling

## Decision: Text Chunking Strategy
**Rationale**: Using 512-token chunks with 50-token overlap to balance context retention and embedding efficiency
**Alternatives considered**:
- Fixed character length (e.g., 1000 chars) - rejected due to inconsistent semantic boundaries
- Sentence-based chunking - rejected due to potential context disruption
- Recursive chunking - rejected due to complexity for initial implementation

## Decision: Cohere Embedding Model
**Rationale**: Using Cohere's embed-multilingual-v3.0 model for educational content with good performance on technical text
**Alternatives considered**:
- OpenAI embeddings - rejected to maintain consistency with tech stack
- Sentence Transformers - rejected due to local resource requirements
- Other Cohere models - embed-multilingual offers best balance of quality and cost

## Decision: Qdrant Collection Schema
**Rationale**: Using vector size of 1024 (Cohere's default) with structured payload for efficient filtering and retrieval
**Alternatives considered**:
- Different vector sizes - 1024 is Cohere's standard output
- Alternative vector databases - Qdrant selected per requirements
- Different indexing strategies - default HNSW provides good performance

## Decision: URL Discovery Method
**Rationale**: Parsing HTML sitemap or using Docusaurus sidebar structure to discover all book pages
**Alternatives considered**:
- Web crawling with link discovery - rejected due to potential dead ends
- Manual URL list - rejected due to maintenance overhead
- Sitemap.xml parsing - selected as primary method with fallbacks

## Decision: Error Handling Strategy
**Rationale**: Implementing retry mechanisms with exponential backoff for API calls and graceful degradation for failed extractions
**Alternatives considered**:
- Fail-fast approach - rejected due to potential for partial indexing
- Complete failure on any error - rejected due to robustness requirements
- Logging with continuation - selected for robust pipeline operation