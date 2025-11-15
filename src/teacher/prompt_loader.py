"""Prompt template loader for English teaching assistant."""

import os
import yaml
from typing import Dict, List, Optional, Any
from pathlib import Path


class PromptLoader:
    """Manages loading and formatting of prompt templates from YAML."""

    def __init__(self, prompts_file: Optional[str] = None):
        """Initialize the prompt loader.

        Args:
            prompts_file: Path to YAML prompts file.
                         Defaults to src/teacher/prompts/prompts.yaml
        """
        if prompts_file is None:
            # Default to prompts.yaml relative to this file
            current_dir = Path(__file__).parent
            prompts_file = current_dir / "prompts" / "prompts.yaml"

        self.prompts_file = Path(prompts_file)

        if not self.prompts_file.exists():
            raise FileNotFoundError(
                f"Prompts file not found: {self.prompts_file}"
            )

        # Load prompts on initialization
        self._prompts: Dict[str, Any] = self._load_yaml()

    def _load_yaml(self) -> Dict[str, Any]:
        """Load prompts from YAML file.

        Returns:
            Dictionary containing all prompts

        Raises:
            yaml.YAMLError: If YAML file is invalid
        """
        try:
            with open(self.prompts_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse YAML: {e}")

    def get_prompt(self, *keys: str) -> Any:
        """Get a prompt by nested keys.

        Args:
            *keys: Nested keys to access the prompt
                  e.g., get_prompt('system_prompt', 'content')

        Returns:
            The requested prompt value

        Raises:
            KeyError: If key path doesn't exist
        """
        result = self._prompts
        for key in keys:
            if isinstance(result, dict):
                if key not in result:
                    raise KeyError(f"Prompt key not found: {'.'.join(keys)}")
                result = result[key]
            else:
                raise KeyError(f"Cannot access key '{key}' in non-dict value")
        return result

    def get_system_prompt(self) -> str:
        """Get the system prompt for the English teacher.

        Returns:
            System prompt string
        """
        return self.get_prompt('system_prompt', 'content')

    def load_greetings(self) -> List[str]:
        """Load all greeting messages.

        Returns:
            List of greeting strings
        """
        greetings_data = self.get_prompt('greetings')

        greetings = []

        # Add first session greeting
        if 'first_session' in greetings_data:
            greetings.append(greetings_data['first_session']['message'])

        # Add returning session greetings
        if 'returning_session' in greetings_data:
            for greeting_item in greetings_data['returning_session']:
                greetings.append(greeting_item['message'])

        return greetings

    def get_summary_prompt(self, conversation_text: str) -> str:
        """Get the summary prompt with conversation text.

        Args:
            conversation_text: The conversation to summarize

        Returns:
            Formatted summary prompt
        """
        template = self.get_prompt('summary_prompt', 'template')
        return template.format(conversation_text=conversation_text)

    def get_error_message(self, error_type: str) -> Dict[str, str]:
        """Get an error message by type.

        Args:
            error_type: Type of error (e.g., 'empty_input', 'transcription_error')

        Returns:
            Dictionary with message and suggestion
        """
        try:
            return self.get_prompt('error_messages', error_type)
        except KeyError:
            return {
                'message': "An error occurred. Please try again.",
                'suggestion': ""
            }

    def get_encouragement(self) -> str:
        """Get a random encouragement message.

        Returns:
            Encouragement string
        """
        import random
        encouragements = self.get_prompt('feedback_prompts', 'encouragement')
        return random.choice(encouragements)

    def get_gentle_correction(
        self,
        student_phrase: str,
        corrected_phrase: str
    ) -> str:
        """Get a gentle correction message.

        Args:
            student_phrase: What the student said
            corrected_phrase: The correct phrase

        Returns:
            Formatted correction message
        """
        template = self.get_prompt(
            'feedback_prompts',
            'gentle_correction',
            'template'
        )
        return template.format(
            student_phrase=student_phrase,
            corrected_phrase=corrected_phrase
        )

    def get_grammar_explanation(
        self,
        rule: str,
        correct_example: str,
        incorrect_example: str,
        tip: str
    ) -> str:
        """Get a formatted grammar explanation.

        Args:
            rule: The grammar rule
            correct_example: Example of correct usage
            incorrect_example: Example of incorrect usage
            tip: Helpful tip for remembering

        Returns:
            Formatted grammar explanation
        """
        template = self.get_prompt(
            'feedback_prompts',
            'grammar_explanation',
            'template'
        )
        return template.format(
            rule=rule,
            correct_example=correct_example,
            incorrect_example=incorrect_example,
            tip=tip
        )

    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the prompts.

        Returns:
            Dictionary with metadata
        """
        return self.get_prompt('metadata')

    def reload(self):
        """Reload prompts from file (useful for development)."""
        self._prompts = self._load_yaml()

    def get_all_prompts(self) -> Dict[str, Any]:
        """Get all prompts as a dictionary.

        Returns:
            Complete prompts dictionary
        """
        return self._prompts.copy()
