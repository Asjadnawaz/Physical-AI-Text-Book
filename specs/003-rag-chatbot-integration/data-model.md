# Data Model: RAG Chatbot Integration

## Entity: ChatSession

**Description**: Represents a user's conversation with the chatbot, including message history and context

**Fields**:
- `id` (string/UUID): Unique identifier for the session
- `user_id` (string/UUID, optional): Identifier for authenticated user (if applicable)
- `created_at` (datetime): Timestamp when session was created
- `updated_at` (datetime): Timestamp when session was last updated
- `messages` (array of Message objects): History of messages in the conversation
- `metadata` (object): Additional session information (e.g., page where chat was initiated)

**Relationships**:
- Contains many Message entities
- Associated with user (optional)

**Validation Rules**:
- `id` must be unique
- `created_at` must be before `updated_at`
- `messages` array must not exceed maximum size to prevent memory issues

## Entity: Message

**Description**: Represents a single message in a chat conversation

**Fields**:
- `id` (string/UUID): Unique identifier for the message
- `session_id` (string/UUID): Reference to the parent ChatSession
- `role` (string): Either "user" or "assistant"
- `content` (string): The text content of the message
- `timestamp` (datetime): When the message was created
- `sources` (array of strings, optional): Citations to textbook sections referenced in the response
- `selected_text` (string, optional): Text selected by user when sending the message (for contextual queries)

**Relationships**:
- Belongs to one ChatSession
- Referenced by ChatSession.messages

**Validation Rules**:
- `role` must be either "user" or "assistant"
- `content` must not be empty
- `session_id` must reference an existing ChatSession

## Entity: RetrievedChunk

**Description**: A segment of textbook content retrieved based on semantic similarity to the user's query

**Fields**:
- `id` (string/UUID): Unique identifier for the chunk
- `textbook_page` (string): Reference to the textbook page/section where this content comes from
- `content` (string): The actual text content of the chunk
- `embedding` (array of floats): Vector representation of the content (stored in Qdrant)
- `similarity_score` (float): How closely this chunk matches the query (0.0 to 1.0)
- `metadata` (object): Additional information like page number, section, etc.

**Relationships**:
- Used by Message entities as source information
- Stored in vector database (Qdrant) for semantic search

**Validation Rules**:
- `similarity_score` must be between 0.0 and 1.0
- `content` must not be empty
- `textbook_page` must reference an existing textbook page

## Entity: UserQuery

**Description**: The input from the user, including selected text context if applicable

**Fields**:
- `id` (string/UUID): Unique identifier for the query
- `session_id` (string/UUID): Reference to the ChatSession
- `query_text` (string): The actual question or text input from the user
- `selected_text` (string, optional): Text selected by user on the page when asking the question
- `timestamp` (datetime): When the query was submitted
- `processed_chunks` (array of RetrievedChunk IDs): Content chunks used to answer this query

**Relationships**:
- Belongs to one ChatSession
- Associated with multiple RetrievedChunk entities

**Validation Rules**:
- `query_text` must not be empty
- `session_id` must reference an existing ChatSession

## Entity: ChatResponse

**Description**: The AI-generated response to the user's query, including citations to textbook sections

**Fields**:
- `id` (string/UUID): Unique identifier for the response
- `query_id` (string/UUID): Reference to the UserQuery this responds to
- `response_text` (string): The AI-generated response text
- `sources` (array of strings): Citations to textbook sections used in the response
- `timestamp` (datetime): When the response was generated
- `confidence_score` (float): Confidence level in the response accuracy (0.0 to 1.0)

**Relationships**:
- Belongs to one UserQuery
- References multiple RetrievedChunk entities as sources

**Validation Rules**:
- `response_text` must not be empty
- `query_id` must reference an existing UserQuery
- `confidence_score` must be between 0.0 and 1.0

## Entity: TextbookContent

**Description**: Represents the processed textbook content that is available for retrieval

**Fields**:
- `id` (string/UUID): Unique identifier for the content block
- `page_path` (string): Path to the textbook page (e.g., "/chapter-1/section-1")
- `section_title` (string): Title of the section
- `content` (string): The text content
- `chunk_index` (integer): Position of this chunk within the page
- `embedding` (array of floats): Vector representation of the content (stored in Qdrant)
- `created_at` (datetime): When this content was processed

**Relationships**:
- Referenced by RetrievedChunk entities
- Stored in vector database (Qdrant) for semantic search

**Validation Rules**:
- `page_path` must reference an existing textbook page
- `content` must not be empty
- `chunk_index` must be non-negative