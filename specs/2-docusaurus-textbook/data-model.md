# Data Model: Docusaurus Textbook Generation

## TextbookSite Entity

**Description**: The main entity representing the complete Docusaurus textbook site with configuration

**Fields**:
- `id`: Unique identifier for the textbook site
- `name`: String, required - The name of the textbook site
- `title`: String, required - The title displayed in the site
- `description`: String, optional - Brief description of the textbook
- `version`: String, optional - Version identifier
- `created_date`: DateTime, required - When the site was created
- `modified_date`: DateTime, required - When the site was last modified
- `config`: JSON, required - Docusaurus configuration object

**Validation Rules**:
- Name must be 1-50 characters, alphanumeric with hyphens/underscores
- Title must be 1-100 characters
- Config must be valid Docusaurus configuration

## Chapter Entity

**Description**: A major division of the textbook content organized as a Docusaurus category

**Fields**:
- `id`: Unique identifier for the chapter
- `title`: String, required - The title of the chapter
- `slug`: String, required - URL-friendly identifier for the chapter
- `position`: Integer, required - Sequential position in the textbook
- `textbook_site_id`: Foreign key reference to TextbookSite entity
- `created_date`: DateTime, required - When the chapter was created
- `modified_date`: DateTime, required - When the chapter was last modified
- `sidebar_label`: String, optional - Label to display in sidebar navigation

**Relationships**:
- Many-to-one with TextbookSite entity (belongs to one site)
- One-to-many with Section entity (contains multiple sections)

**Validation Rules**:
- Title must be 1-100 characters
- Slug must be URL-friendly (alphanumeric, hyphens, underscores)
- Position must be positive integer
- Must belong to a valid textbook site

## Section Entity

**Description**: A subdivision within a chapter organized as a Docusaurus document

**Fields**:
- `id`: Unique identifier for the section
- `title`: String, required - The title of the section
- `slug`: String, required - URL-friendly identifier for the section
- `position`: Integer, required - Sequential position within the chapter
- `content`: Text, required - The main content of the section in Markdown/MDX
- `chapter_id`: Foreign key reference to Chapter entity
- `created_date`: DateTime, required - When the section was created
- `modified_date`: DateTime, required - When the section was last modified
- `sidebar_label`: String, optional - Label to display in sidebar navigation
- `custom_edit_url`: String, optional - Custom URL for edit link

**Relationships**:
- Many-to-one with Chapter entity (belongs to one chapter)

**Validation Rules**:
- Title must be 1-100 characters
- Content must not be empty
- Position must be positive integer
- Must belong to a valid chapter

## NavigationConfig Entity

**Description**: The configuration that defines sidebar navigation structure

**Fields**:
- `id`: Unique identifier for the navigation config
- `config_type`: String, required - Type of navigation config (sidebar, topnav, etc.)
- `config_data`: JSON, required - The actual navigation configuration
- `textbook_site_id`: Foreign key reference to TextbookSite entity
- `created_date`: DateTime, required - When the config was created
- `modified_date`: DateTime, required - When the config was last modified

**Validation Rules**:
- Config type must be from predefined list (sidebar, topnav)
- Config data must be valid Docusaurus navigation configuration
- Must belong to a valid textbook site

## ThemeConfig Entity

**Description**: The configuration for site styling and appearance

**Fields**:
- `id`: Unique identifier for the theme config
- `theme_name`: String, optional - Name of the theme
- `theme_config`: JSON, required - Theme configuration object
- `textbook_site_id`: Foreign key reference to TextbookSite entity
- `created_date`: DateTime, required - When the config was created
- `modified_date`: DateTime, required - When the config was last modified

**Validation Rules**:
- Theme config must be valid Docusaurus theme configuration
- Must belong to a valid textbook site