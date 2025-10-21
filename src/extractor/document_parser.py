"""
Document parser for local files (text, PDF, etc.)
"""
import os
from typing import Dict
from PyPDF2 import PdfReader


class DocumentParser:
    """Parse local documents into text content."""

    def parse_file(self, file_path: str) -> Dict[str, str]:
        """
        Parse a local file and extract text content.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with filename, content, and source_type
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        if ext == '.pdf':
            content = self._parse_pdf(file_path)
        elif ext in ['.txt', '.md', '.markdown']:
            content = self._parse_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        return {
            'title': filename,
            'url': file_path,
            'content': content,
            'source_type': 'file'
        }

    def _parse_text(self, file_path: str) -> str:
        """Parse plain text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _parse_pdf(self, file_path: str) -> str:
        """Parse PDF file."""
        try:
            reader = PdfReader(file_path)
            text_parts = []

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            return '\n\n'.join(text_parts)

        except Exception as e:
            raise Exception(f"Failed to parse PDF {file_path}: {str(e)}")

    def parse_multiple(self, file_paths: list) -> list:
        """
        Parse multiple files.

        Args:
            file_paths: List of file paths

        Returns:
            List of parsed content dictionaries
        """
        results = []

        for file_path in file_paths:
            try:
                print(f"Parsing: {file_path}")
                result = self.parse_file(file_path)
                results.append(result)
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")
                continue

        return results
