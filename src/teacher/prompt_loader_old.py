"""Prompt template loader for English teaching assistant."""

import os
from typing import Dict, List, Optional
from pathlib import Path


class PromptLoader:
    """Manages loading and formatting of prompt templates."""

    def __init__(self, prompts_dir: Optional[str] = None):
        """Initialize the prompt loader.

        Args:
            prompts_dir: Directory containing prompt templates.
                        Defaults to src/teacher/prompts/
        """
        if prompts_dir is None:
            # Default to prompts directory relative to this file
            current_dir = Path(__file__).parent
            prompts_dir = current_dir / "prompts"

        self.prompts_dir = Path(prompts_dir)

        if not self.prompts_dir.exists():
            raise FileNotFoundError(
                f"Prompts directory not found: {self.prompts_dir}"
            )

        # Cache for loaded prompts
        self._cache: Dict[str, str] = {}
        self._greetings_cache: Optional[List[str]] = None

    def load_prompt(self, template_name: str) -> str:
        """Load a prompt template from file.

        Args:
            template_name: Name of the template file (without .txt extension)

        Returns:
            The prompt template content

        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        # Check cache first
        if template_name in self._cache:
            return self._cache[template_name]

        # Load from file
        template_path = self.prompts_dir / f"{template_name}.txt"

        if not template_path.exists():
            raise FileNotFoundError(
                f"Prompt template not found: {template_path}"
            )

        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # Cache the content
        self._cache[template_name] = content

        return content

    def format_prompt(self, template_name: str, **kwargs) -> str:
        """Load and format a prompt template with variables.

        Args:
            template_name: Name of the template file
            **kwargs: Variables to substitute in the template

        Returns:
            Formatted prompt string
        """
        template = self.load_prompt(template_name)
        return template.format(**kwargs)

    def load_greetings(self) -> List[str]:
        """Load all greeting messages.

        Returns:
            List of greeting strings
        """
        if self._greetings_cache is not None:
            return self._greetings_cache

        greetings_content = self.load_prompt("greetings")

        # Greetings are separated by "---"
        greetings = [
            g.strip()
            for g in greetings_content.split("---")
            if g.strip()
        ]

        self._greetings_cache = greetings
        return greetings

    def get_system_prompt(self) -> str:
        """Get the system prompt for the English teacher.

        Returns:
            System prompt string
        """
        return self.load_prompt("system_prompt")

    def get_summary_prompt(self, conversation_text: str) -> str:
        """Get the summary prompt with conversation text.

        Args:
            conversation_text: The conversation to summarize

        Returns:
            Formatted summary prompt
        """
        return self.format_prompt(
            "summary_prompt",
            conversation_text=conversation_text
        )

    def clear_cache(self):
        """Clear the prompt cache."""
        self._cache.clear()
        self._greetings_cache = None

    def reload_prompts(self):
        """Reload all prompts from disk (useful for development)."""
        self.clear_cache()
