"""
Database storage layer for extracted content.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os


class Storage:
    """Manages SQLite database for storing extracted content."""

    def __init__(self, db_path: str = "data/database.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Content table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                source_type TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Persona profile table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persona_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                analysis TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def add_content(self, source: str, source_type: str, content: str, metadata: str = None):
        """Add extracted content to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO content (source, source_type, content, metadata)
            VALUES (?, ?, ?, ?)
        """, (source, source_type, content, metadata))

        conn.commit()
        content_id = cursor.lastrowid
        conn.close()

        return content_id

    def get_all_content(self) -> List[Dict]:
        """Retrieve all content from database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM content ORDER BY created_at DESC")
        rows = cursor.fetchall()

        content = [dict(row) for row in rows]
        conn.close()

        return content

    def save_persona_profile(self, name: str, analysis: str):
        """Save or update persona profile."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if profile exists
        cursor.execute("SELECT id FROM persona_profile WHERE name = ?", (name,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE persona_profile
                SET analysis = ?, updated_at = CURRENT_TIMESTAMP
                WHERE name = ?
            """, (analysis, name))
        else:
            cursor.execute("""
                INSERT INTO persona_profile (name, analysis)
                VALUES (?, ?)
            """, (name, analysis))

        conn.commit()
        conn.close()

    def get_persona_profile(self, name: str) -> Optional[Dict]:
        """Retrieve persona profile."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM persona_profile WHERE name = ?", (name,))
        row = cursor.fetchone()

        profile = dict(row) if row else None
        conn.close()

        return profile

    def get_content_count(self) -> int:
        """Get total number of content items."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM content")
        count = cursor.fetchone()[0]

        conn.close()
        return count
