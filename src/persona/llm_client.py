"""
LLM client for interacting with OpenAI or Anthropic APIs.
"""
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv('config/.env')


class LLMClient:
    """Unified client for LLM APIs (OpenAI or Anthropic)."""

    def __init__(self, provider: Optional[str] = None):
        """
        Initialize LLM client.

        Args:
            provider: LLM provider ('openai' or 'anthropic')
        """
        self.provider = provider or os.getenv('LLM_PROVIDER', 'openai').lower()

        if self.provider == 'openai':
            import openai
            self.api_key = os.getenv('OPENAI_API_KEY')
            self.model = os.getenv('OPENAI_MODEL', 'gpt-4o')
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            self.client = openai.OpenAI(api_key=self.api_key)

        elif self.provider == 'anthropic':
            import anthropic
            self.api_key = os.getenv('ANTHROPIC_API_KEY')
            self.model = os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
            self.client = anthropic.Anthropic(api_key=self.api_key)

        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def generate(self, messages: List[Dict[str, str]],
                 system: Optional[str] = None,
                 max_tokens: int = 4000,
                 temperature: float = 0.7) -> str:
        """
        Generate a response from the LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
            system: System prompt (optional)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text response
        """
        if self.provider == 'openai':
            return self._generate_openai(messages, system, max_tokens, temperature)
        elif self.provider == 'anthropic':
            return self._generate_anthropic(messages, system, max_tokens, temperature)

    def _generate_openai(self, messages: List[Dict], system: Optional[str],
                         max_tokens: int, temperature: float) -> str:
        """Generate response using OpenAI API."""
        # Add system message if provided
        if system:
            messages = [{"role": "system", "content": system}] + messages

        # Use max_completion_tokens for newer models, max_tokens for older ones
        completion_params = {
            "model": self.model,
            "messages": messages
        }

        # Some models only support default temperature
        if 'gpt-5' in self.model or 'o1' in self.model or 'o3' in self.model:
            # These models only support temperature=1 or no temperature parameter
            pass  # Skip temperature parameter for these models
        else:
            completion_params["temperature"] = temperature

        # Newer models (gpt-4o, gpt-4-turbo, etc.) use max_completion_tokens
        if 'gpt-4' in self.model or 'gpt-5' in self.model:
            completion_params["max_completion_tokens"] = max_tokens
        else:
            completion_params["max_tokens"] = max_tokens

        response = self.client.chat.completions.create(**completion_params)

        return response.choices[0].message.content

    def _generate_anthropic(self, messages: List[Dict], system: Optional[str],
                           max_tokens: int, temperature: float) -> str:
        """Generate response using Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "",
            messages=messages
        )

        return response.content[0].text

    def analyze_text(self, text: str, prompt: str, max_tokens: int = 2000) -> str:
        """
        Analyze text with a specific prompt.

        Args:
            text: Text to analyze
            prompt: Analysis prompt
            max_tokens: Maximum tokens to generate

        Returns:
            Analysis result
        """
        messages = [
            {
                "role": "user",
                "content": f"{prompt}\n\n---\n\nText to analyze:\n{text}"
            }
        ]

        return self.generate(messages, max_tokens=max_tokens, temperature=0.3)
