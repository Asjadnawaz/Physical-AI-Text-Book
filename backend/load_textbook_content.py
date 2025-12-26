#!/usr/bin/env python3
"""
Script to initialize the textbook content in the vector database
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.textbook_content_service import TextbookContentService


def main():
    """
    Main function to process textbook content and load it into the vector database
    """
    print("Starting textbook content processing...")

    # Create the content service
    content_service = TextbookContentService()

    # Process all textbook content
    content_service.process_textbook_content()

    print("Textbook content processing completed!")


if __name__ == "__main__":
    main()