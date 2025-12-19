# Quickstart: Textbook Generation

## Prerequisites

- Python 3.11 or higher
- Pandoc (for document format conversion)
- WeasyPrint (for PDF generation)
- Git (for version control)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install system dependencies:
   - Install Pandoc: https://pandoc.org/installing.html
   - Install WeasyPrint dependencies (Cairo, Pango, etc.)

## Basic Usage

### Generate a Simple Textbook

1. Prepare your textbook content in the required format (JSON structure with chapters and sections)

2. Run the textbook generator:
   ```bash
   python -m src.cli.textbook_generator --input textbook.json --output my_textbook.pdf
   ```

### Export to Different Formats

```bash
# Generate PDF
python -m src.cli.textbook_generator --input textbook.json --output my_textbook.pdf --format pdf

# Generate HTML
python -m src.cli.textbook_generator --input textbook.json --output my_textbook.html --format html

# Generate EPUB
python -m src.cli.textbook_generator --input textbook.json --output my_textbook.epub --format epub
```

### Customize Styling

You can provide a custom CSS file for styling:

```bash
python -m src.cli.textbook_generator --input textbook.json --output my_textbook.pdf --css custom_style.css
```

## Example Content Structure

```json
{
  "title": "Introduction to Physical AI",
  "author": "Educator Name",
  "subject": "Physical AI",
  "chapters": [
    {
      "number": 1,
      "title": "What is Physical AI?",
      "sections": [
        {
          "number": 1,
          "title": "Definition and Concepts",
          "content": "Physical AI is a field that combines artificial intelligence with physical systems..."
        }
      ]
    }
  ]
}
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/unit/test_generation_service.py

# Run with coverage
pytest --cov=src
```

## Development

1. Activate your virtual environment
2. Make changes to the source code
3. Run tests to ensure functionality
4. Generate sample textbooks to test your changes

## Troubleshooting

- If PDF generation fails, ensure WeasyPrint dependencies are properly installed
- For large textbooks, ensure sufficient memory is available
- For format conversion issues, check Pandoc installation and version compatibility