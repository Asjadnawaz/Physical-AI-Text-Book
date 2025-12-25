<!-- Sync Impact Report (Initial Creation):
Version: 1.0.0 (new)
Affected Files: docusaurus.config.js, sidebars.js, all /docs/*.md files (to be created), root README.
No conflicts detected. -->

<!-- Sync Impact Report (Updated for RAG Chatbot Integration):
Version: 1.0.0 → 2.0.0
Added sections: RAG Chatbot Integration Principles
Modified principles: Technical Implementation Standards (expanded to include new tech stack)
Modified principles: Content Quality and Consistency (added chatbot interaction considerations)
Modified principles: Compliance and Review (added chatbot validation requirements)
Templates requiring updates: plan-template.md, spec-template.md, tasks-template.md ✅ updated
Follow-up TODOs: None
 -->

# Physical AI & Humanoid Robotics: An Online Technical Textbook Constitution

## Core Principles

### Educational Clarity and Accessibility
Prioritize beginner-friendly language: Use simple explanations, real-world analogies (e.g., ROS 2 as the "nervous system" of a robot), and gradual introduction of technical terms. Concept-first approach: Explain ideas before introducing specific tools or code. Avoid overwhelming details: Limit code snippets, complex math, or advanced topics unless essential for understanding.

### Professional Structure and Flow
Strictly adhere to the predefined course outline: Include all specified sections (Preface/Introduction, Why Physical AI Matters, Course Overview, Modules 1–4, Capstone Project, Weekly Breakdown, Learning Outcomes, Assessments, Hardware Requirements). Logical progression: Build from basics (e.g., ROS 2 fundamentals) to advanced (e.g., Vision-Language-Action models) and integration (Capstone). Hierarchical organization: Use Docusaurus categories for modules and sub-sections for chapters.

### Content Quality and Consistency
Conceptual and non-technical tone: Focus on "why" and "what" rather than deep implementation. Where tools are mentioned (e.g., ROS 2, Gazebo, NVIDIA Isaac), emphasize purpose and high-level usage. Neutral and advisory: Avoid marketing language (e.g., no hype about tools or companies). Use simple, advisory tone for practical sections like Hardware Requirements. Inclusivity: Target students, hobbyists, and professionals new to Physical AI; highlight transformative potential (e.g., skill enhancement, not job loss). When integrating chatbot interactions, maintain educational integrity and ensure responses align with textbook content.

### Technical Implementation Standards
Built with Docusaurus: Use Markdown/MDX files in a /docs folder with folder-based categories for hierarchy. Configure sidebars.js for nested navigation matching the outline. Single-instance docs plugin: No versioning initially; focus on current content. Readability enhancements: Include headings, lists, admonitions (e.g., notes, warnings), and optional diagrams (text-based or described for future images). SEO and usability: Clear titles, intros, and summaries per page. For RAG chatbot integration: Strictly use Docusaurus (frontend), FastAPI (backend), Qdrant (vector DB), OpenAI Agents SDK with Gemini API (AI layer), ChatKit SDK (chat handling), and Neon Postgres (metadata/session storage). No unauthorized additions.

### Accuracy and Content Fidelity
The chatbot must ONLY use textbook content: No external internet knowledge, general AI training data, or hallucinations allowed. Answers are generated strictly from retrieved or selected text chunks. Semantic search priority: Use vector embeddings for meaning-based retrieval over keyword matching to ensure relevant, context-aware responses. Citation and transparency: Responses should cite or reference specific book sections to maintain educational integrity.

### User Experience and Interactivity
Seamless integration: Embed the chat UI within the Docusaurus website, supporting text selection for targeted queries and maintaining conversational context. Beginner-friendly: Provide clear, human-like answers in an educational tone, avoiding jargon unless explained from the book. Responsiveness: Ensure low-latency interactions, with retrieval and generation optimized for real-time use.

### Performance and Scalability
Efficient retrieval: Limit retrieved chunks to relevant sections to minimize processing time and costs. Use Qdrant free tier optimizations. Testing standards: Implement unit tests for chunking, embedding, retrieval, and generation; integration tests for end-to-end flow; ensure 100% coverage for critical paths like selected-text queries. Monitoring: Log queries and responses in Postgres for quality review, without storing sensitive user data.

### Compliance and Review
All content must align with this constitution. Before completion: Validate against checklist (all modules included, outline followed, clear explanations, logical flow, end-to-end capstone). Future expansions: Use SpecifyPlus workflows if extending (e.g., new features as specs). For RAG chatbot: Before deployment, verify no hallucinations, full tech stack integration, and seamless website embedding.

## Governance
Amendments require explicit updates with semantic versioning (MAJOR for structural changes, MINOR for new content additions, PATCH for corrections). For RAG chatbot integration: Amendments require explicit updates with semantic versioning (MAJOR for architectural changes, MINOR for feature additions, PATCH for bug fixes or refinements). All changes must align with the educational accuracy and control requirements.

All content must align with this constitution. Amendments require explicit updates with semantic versioning (MAJOR for structural changes, MINOR for new content additions, PATCH for corrections). Before completion: Validate against checklist (all modules included, outline followed, clear explanations, logical flow, end-to-end capstone).

**Version**: 2.0.0 | **Ratified**: 2025-12-19 | **Last Amended**: 2025-12-19