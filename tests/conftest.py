"""Pytest configuration and shared fixtures."""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Generator
import pytest


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for tests.

    Yields:
        Path to temporary directory
    """
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_env_vars(monkeypatch) -> None:
    """Set up mock environment variables for tests.

    Args:
        monkeypatch: Pytest monkeypatch fixture
    """
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-123")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("TEACHER_MODEL", "gpt-4o")


@pytest.fixture
def sample_conversation() -> list:
    """Create sample conversation data for testing.

    Returns:
        List of conversation messages
    """
    return [
        {
            "role": "user",
            "content": "Hello, I want to practice English.",
            "timestamp": "2025-01-15T10:00:00"
        },
        {
            "role": "assistant",
            "content": "Great! I'm here to help you practice. What would you like to talk about?",
            "timestamp": "2025-01-15T10:00:05"
        },
        {
            "role": "user",
            "content": "Can we talk about traveling?",
            "timestamp": "2025-01-15T10:00:15"
        },
        {
            "role": "assistant",
            "content": "Absolutely! Traveling is a wonderful topic. Where would you like to visit?",
            "timestamp": "2025-01-15T10:00:20"
        }
    ]


@pytest.fixture
def prompts_file(temp_dir: str) -> str:
    """Create a temporary YAML prompts file for testing.

    Args:
        temp_dir: Temporary directory path

    Returns:
        Path to prompts YAML file
    """
    # Copy test prompts file to temp directory
    source = Path(__file__).parent / "fixtures" / "test_prompts.yaml"
    dest = Path(temp_dir) / "prompts.yaml"

    shutil.copy(source, dest)

    return str(dest)
