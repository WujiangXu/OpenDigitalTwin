"""Unit tests for PromptLoader (YAML-based)."""

import pytest
from pathlib import Path
from src.teacher.prompt_loader import PromptLoader


class TestPromptLoader:
    """Test cases for PromptLoader class with YAML."""

    def test_init_with_valid_file(self, prompts_file):
        """Test initialization with valid YAML file."""
        loader = PromptLoader(prompts_file)
        assert loader.prompts_file == Path(prompts_file)
        assert loader._prompts is not None

    def test_init_with_invalid_file(self, temp_dir):
        """Test initialization with non-existent file."""
        invalid_path = Path(temp_dir) / "nonexistent.yaml"
        with pytest.raises(FileNotFoundError):
            PromptLoader(str(invalid_path))

    def test_get_prompt_success(self, prompts_file):
        """Test successful nested prompt retrieval."""
        loader = PromptLoader(prompts_file)
        content = loader.get_prompt('system_prompt', 'content')
        assert content == "You are a test English teaching assistant."

    def test_get_prompt_not_found(self, prompts_file):
        """Test getting non-existent prompt."""
        loader = PromptLoader(prompts_file)
        with pytest.raises(KeyError):
            loader.get_prompt('nonexistent_key')

    def test_get_system_prompt(self, prompts_file):
        """Test getting system prompt."""
        loader = PromptLoader(prompts_file)
        system_prompt = loader.get_system_prompt()
        assert system_prompt == "You are a test English teaching assistant."

    def test_load_greetings(self, prompts_file):
        """Test loading greeting messages."""
        loader = PromptLoader(prompts_file)
        greetings = loader.load_greetings()

        assert len(greetings) == 3
        assert greetings[0] == "Hello test!"
        assert "Hi there test!" in greetings
        assert "Welcome test!" in greetings

    def test_get_summary_prompt(self, prompts_file):
        """Test getting formatted summary prompt."""
        loader = PromptLoader(prompts_file)
        summary_prompt = loader.get_summary_prompt("My conversation text")

        assert "My conversation text" in summary_prompt
        assert "Summarize" in summary_prompt

    def test_get_error_message(self, prompts_file):
        """Test getting error message."""
        loader = PromptLoader(prompts_file)
        error_msg = loader.get_error_message('empty_input')

        assert 'message' in error_msg
        assert 'suggestion' in error_msg
        assert error_msg['message'] == "Test error message"

    def test_get_error_message_not_found(self, prompts_file):
        """Test getting non-existent error message returns default."""
        loader = PromptLoader(prompts_file)
        error_msg = loader.get_error_message('nonexistent_error')

        assert 'message' in error_msg
        assert "An error occurred" in error_msg['message']

    def test_get_encouragement(self, prompts_file):
        """Test getting random encouragement."""
        loader = PromptLoader(prompts_file)
        encouragement = loader.get_encouragement()

        assert encouragement in ["Great!", "Good job!"]

    def test_get_gentle_correction(self, prompts_file):
        """Test getting gentle correction message."""
        loader = PromptLoader(prompts_file)
        correction = loader.get_gentle_correction(
            student_phrase="I goed home",
            corrected_phrase="I went home"
        )

        assert "I goed home" in correction
        assert "I went home" in correction

    def test_get_grammar_explanation(self, prompts_file):
        """Test getting grammar explanation."""
        loader = PromptLoader(prompts_file)
        explanation = loader.get_grammar_explanation(
            rule="Use 'went' for past tense of 'go'",
            correct_example="I went home",
            incorrect_example="I goed home",
            tip="Remember: go -> went"
        )

        assert "went" in explanation
        assert "I went home" in explanation

    def test_get_metadata(self, prompts_file):
        """Test getting metadata."""
        loader = PromptLoader(prompts_file)
        metadata = loader.get_metadata()

        assert 'last_updated' in metadata
        assert 'author' in metadata

    def test_reload(self, prompts_file):
        """Test reloading prompts."""
        loader = PromptLoader(prompts_file)

        # Get initial prompts
        prompts1 = loader.get_all_prompts()

        # Reload
        loader.reload()

        # Get reloaded prompts
        prompts2 = loader.get_all_prompts()

        # Should be equal
        assert prompts1 == prompts2

    def test_get_all_prompts(self, prompts_file):
        """Test getting all prompts."""
        loader = PromptLoader(prompts_file)
        all_prompts = loader.get_all_prompts()

        assert 'system_prompt' in all_prompts
        assert 'greetings' in all_prompts
        assert 'metadata' in all_prompts
