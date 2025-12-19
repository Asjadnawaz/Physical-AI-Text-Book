---
id: 1
title: Create Textbook Constitution
stage: constitution
date: 2025-12-19
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: Claude Code
command: sp.constitution
labels: ["constitution", "textbook", "physical-ai", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
Project Constitution for Physical AI & Humanoid Robotics Online Textbook
Project Name: Physical AI & Humanoid Robotics: An Online Technical Textbook
Project Description:
This project creates a professional, beginner-friendly online textbook as a static website built with Docusaurus. The textbook teaches Physical AI and Humanoid Robotics, structured like a university course with modules, chapters, and educational content. It follows a predefined course outline, emphasizing conceptual understanding before tools, clear explanations, analogies, and minimal code examples.
Version: 1.0.0
Date Established: December 19, 2025
Governance: Amendments require explicit updates with semantic versioning (MAJOR for structural changes, MINOR for new content additions, PATCH for corrections).
Core Principles

Educational Clarity and Accessibility
Prioritize beginner-friendly language: Use simple explanations, real-world analogies (e.g., ROS 2 as the "nervous system" of a robot), and gradual introduction of technical terms.
Concept-first approach: Explain ideas before introducing specific tools or code.
Avoid overwhelming details: Limit code snippets, complex math, or advanced topics unless essential for understanding.

Professional Structure and Flow
Strictly adhere to the predefined course outline: Include all specified sections (Preface/Introduction, Why Physical AI Matters, Course Overview, Modules 1–4, Capstone Project, Weekly Breakdown, Learning Outcomes, Assessments, Hardware Requirements).
Logical progression: Build from basics (e.g., ROS 2 fundamentals) to advanced (e.g., Vision-Language-Action models) and integration (Capstone).
Hierarchical organization: Use Docusaurus categories for modules and sub-sections for chapters.

Content Quality and Consistency
Conceptual and non-technical tone: Focus on "why" and "what" rather than deep implementation. Where tools are mentioned (e.g., ROS 2, Gazebo, NVIDIA Isaac), emphasize purpose and high-level usage.
Neutral and advisory: Avoid marketing language (e.g., no hype about tools or companies). Use simple, advisory tone for practical sections like Hardware Requirements.
Inclusivity: Target students, hobbyists, and professionals new to Physical AI; highlight transformative potential (e.g., skill enhancement, not job loss).

Technical Implementation Standards
Built with Docusaurus: Use Markdown/MDX files in a /docs folder with folder-based categories for hierarchy. Configure sidebars.js for nested navigation matching the outline.
Single-instance docs plugin: No versioning initially; focus on current content.
Readability enhancements: Include headings, lists, admonitions (e.g., notes, warnings), and optional diagrams (text-based or described for future images).
SEO and usability: Clear titles, intros, and summaries per page.

Compliance and Review
All content must align with this constitution.
Before completion: Validate against checklist (all modules included, outline followed, clear explanations, logical flow, end-to-end capstone).
Future expansions: Use SpecifyPlus workflows if extending (e.g., new features as specs).


Sync Impact Report (Initial Creation):

Version: 1.0.0 (new)
Affected Files: docusaurus.config.js, sidebars.js, all /docs/*.md files (to be created), root README.
No conflicts detected.
```

## Response snapshot

Updated the project constitution at `.specify/memory/constitution.md` with the Physical AI & Humanoid Robotics textbook project details. The constitution now includes five core principles:

1. Educational Clarity and Accessibility
2. Professional Structure and Flow
3. Content Quality and Consistency
4. Technical Implementation Standards
5. Compliance and Review

The constitution defines governance rules with semantic versioning for amendments and establishes the project's foundational principles for creating a beginner-friendly online textbook about Physical AI and Humanoid Robotics using Docusaurus.

## Outcome

- ✅ Impact: New constitution created for Physical AI textbook project
- 🧪 Tests: none
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Create textbook content following constitution guidelines
- 🧠 Reflection: Constitution successfully updated with all required principles and governance structure

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - Constitution properly formatted and contains all required elements
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin creating textbook content following the established constitution