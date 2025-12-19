# Data Model: Textbook Generation

## Textbook Entity

**Description**: The main entity representing the complete textbook with metadata

**Fields**:
- `id`: Unique identifier for the textbook
- `title`: String, required - The title of the textbook
- `author`: String, optional - The author name(s)
- `subject`: String, required - The subject area of the textbook
- `description`: String, optional - Brief description of the textbook content
- `created_date`: DateTime, required - When the textbook was created
- `modified_date`: DateTime, required - When the textbook was last modified
- `version`: String, optional - Version identifier
- `language`: String, default "English" - Language of the textbook content

**Relationships**:
- One-to-many with Chapter entity (contains multiple chapters)

**Validation Rules**:
- Title must be 1-200 characters
- Subject must be selected from predefined list
- Language must be from supported languages list

## Chapter Entity

**Description**: A major division of the textbook containing multiple sections and content

**Fields**:
- `id`: Unique identifier for the chapter
- `title`: String, required - The title of the chapter
- `number`: Integer, required - Sequential number of the chapter
- `description`: String, optional - Brief description of the chapter content
- `textbook_id`: Foreign key reference to Textbook entity
- `created_date`: DateTime, required - When the chapter was created
- `modified_date`: DateTime, required - When the chapter was last modified

**Relationships**:
- Many-to-one with Textbook entity (belongs to one textbook)
- One-to-many with Section entity (contains multiple sections)

**Validation Rules**:
- Title must be 1-100 characters
- Number must be positive integer
- Must belong to a valid textbook

## Section Entity

**Description**: A subdivision within a chapter containing specific content on a topic

**Fields**:
- `id`: Unique identifier for the section
- `title`: String, required - The title of the section
- `number`: Integer, required - Sequential number of the section within the chapter
- `content`: Text, required - The main content of the section
- `chapter_id`: Foreign key reference to Chapter entity
- `created_date`: DateTime, required - When the section was created
- `modified_date`: DateTime, required - When the section was last modified
- `section_type`: String, optional - Type of section (text, exercise, example, etc.)

**Relationships**:
- Many-to-one with Chapter entity (belongs to one chapter)
- One-to-many with ContentBlock entity (contains multiple content blocks)

**Validation Rules**:
- Title must be 1-100 characters
- Content must not be empty
- Number must be positive integer
- Must belong to a valid chapter

## ContentBlock Entity

**Description**: Individual pieces of content within sections (text, images, exercises, etc.)

**Fields**:
- `id`: Unique identifier for the content block
- `content_type`: String, required - Type of content (text, image, exercise, example, etc.)
- `content_data`: Text/JSON, required - The actual content data
- `position`: Integer, required - Position order within the section
- `section_id`: Foreign key reference to Section entity
- `created_date`: DateTime, required - When the content block was created
- `modified_date`: DateTime, required - When the content block was last modified
- `metadata`: JSON, optional - Additional metadata for the content block

**Relationships**:
- Many-to-one with Section entity (belongs to one section)

**Validation Rules**:
- Content type must be from predefined list
- Position must be positive integer
- Must belong to a valid section

## ExportFormat Entity

**Description**: The format specification for different output types (PDF, HTML, EPUB)

**Fields**:
- `id`: Unique identifier for the export format
- `format_name`: String, required - Name of the format (PDF, HTML, EPUB)
- `format_code`: String, required - Short code for the format (pdf, html, epub)
- `description`: String, optional - Description of the format characteristics
- `default_template`: String, optional - Default template path for this format
- `supported_features`: JSON, optional - Features supported by this format
- `created_date`: DateTime, required - When the format was defined
- `modified_date`: DateTime, required - When the format was last modified

**Validation Rules**:
- Format name and code must be unique
- Format code must be from predefined list (pdf, html, epub, docx)
- Default template must exist if specified