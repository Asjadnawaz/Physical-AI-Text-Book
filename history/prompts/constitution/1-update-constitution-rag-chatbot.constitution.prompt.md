---
id: 1
title: Update Constitution RAG Chatbot
stage: constitution
date: 2025-12-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: sp.constitution
labels: [constitution,rag,chatbot,physical-ai]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - constitution validation
---

## Prompt

```text
add"Project Name: RAG Chatbot for Physical AI & Humanoid Robotics Textbook
Project Description:
This project develops a Retrieval-Augmented Generation (RAG) chatbot integrated into the Docusaurus-based online textbook website. The chatbot answers user questions exclusively from the textbook's content, using semantic search and AI generation to provide accurate, syllabus-aligned responses. It supports global queries and answers based on user-selected text, acting as an interactive teaching assistant. The implementation follows a specified tech stack including FastAPI, Qdrant, OpenAI Agents SDK, ChatKit SDK, and Neon Postgres, ensuring no external knowledge or hallucinations.
Version: 1.0.0
Date Established: December 19, 2025
Governance: Amendments require explicit updates with semantic versioning (MAJOR for architectural changes, MINOR for feature additions, PATCH for bug fixes or refinements). All changes must align with the educational accuracy and control requirements.
Core Principles

Accuracy and Content Fidelity
The chatbot must ONLY use textbook content: No external internet knowledge, general AI training data, or hallucinations allowed. Answers are generated strictly from retrieved or selected text chunks.
Semantic search priority: Use vector embeddings for meaning-based retrieval over keyword matching to ensure relevant, context-aware responses.
Citation and transparency: Responses should cite or reference specific book sections to maintain educational integrity.

User Experience and Interactivity
Seamless integration: Embed the chat UI within the Docusaurus website, supporting text selection for targeted queries and maintaining conversational context.
Beginner-friendly: Provide clear, human-like answers in an educational tone, avoiding jargon unless explained from the book.
Responsiveness: Ensure low-latency interactions, with retrieval and generation optimized for real-time use.

Technical Reliability and Security
Tech stack adherence: Strictly use Docusaurus (frontend), FastAPI (backend), Qdrant (vector DB), OpenAI Agents SDK with Gemini API (AI layer), ChatKit SDK (chat handling), and Neon Postgres (metadata/session storage). No unauthorized additions.
Data handling: Chunk textbook content appropriately, generate embeddings securely, and store sessions to support user-specific interactions without compromising privacy.
Error handling: Gracefully manage out-of-scope queries by redirecting to book content or indicating limitations.

Performance and Scalability
Efficient retrieval: Limit retrieved chunks to relevant sections to minimize processing time and costs. Use Qdrant free tier optimizations.
Testing standards: Implement unit tests for chunking, embedding, retrieval, and generation; integration tests for end-to-end flow; ensure 100% coverage for critical paths like selected-text queries.
Monitoring: Log queries and responses in Postgres for quality review, without storing sensitive user data.

Compliance and Review
Educational alignment: All features must enhance learning (e.g., as a smart tutor) without deviating from the syllabus.
Workflow adherence: Use SpecifyPlus commands for specs, plans, tasks, and implementation to maintain structured development.
Final validation: Before deployment, verify no hallucinations, full tech stack integration, and seamless website embedding.


Sync Impact Report (Initial Creation):

Version: 1.0.0 (new)
Affected Files: docusaurus.config.js (for chat embedding), backend FastAPI routes, Qdrant setup scripts, OpenAI Agents integration, Neon Postgres schemas, and new docs for chatbot usage.
No conflicts detected; aligns with existing textbook project."
```

## Response snapshot

I have successfully updated the project constitution to incorporate the RAG Chatbot project while maintaining the original textbook project principles. The updated constitution now includes:

1. Added new principles specific to the RAG Chatbot integration:
   - Accuracy and Content Fidelity: Ensures the chatbot only uses textbook content
   - User Experience and Interactivity: Focuses on seamless integration and beginner-friendly responses
   - Performance and Scalability: Addresses efficient retrieval and testing standards

2. Modified existing principles to accommodate the chatbot:
   - Technical Implementation Standards: Expanded to include the new tech stack (Docusaurus, FastAPI, Qdrant, OpenAI Agents SDK, ChatKit SDK, Neon Postgres)
   - Content Quality and Consistency: Added chatbot interaction considerations
   - Compliance and Review: Added chatbot validation requirements

3. Updated governance sections to reflect both the original textbook project and the new RAG chatbot integration

4. Version has been incremented from 1.0.0 to 2.0.0 to reflect the significant architectural addition of the RAG chatbot system

The constitution now properly governs both the original textbook project and the new RAG chatbot integration, ensuring that all development aligns with educational accuracy and control requirements while maintaining the pedagogical quality of the original textbook project.

## Outcome

- ✅ Impact: Updated constitution to include RAG chatbot principles while preserving original textbook project principles
- 🧪 Tests: Constitution validation performed
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Ready for specification of RAG chatbot features
- 🧠 Reflection: Successfully integrated new project scope while maintaining educational integrity

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin specification of RAG chatbot features