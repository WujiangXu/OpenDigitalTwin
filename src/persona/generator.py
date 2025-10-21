"""
Response generator that uses persona to generate authentic responses.
"""
from typing import List, Dict, Optional
from .llm_client import LLMClient
from extractor.storage import Storage


class ResponseGenerator:
    """Generates responses using persona profile and relevant context."""

    def __init__(self, llm_client: LLMClient = None, storage: Storage = None):
        """
        Initialize response generator.

        Args:
            llm_client: LLM client instance
            storage: Storage instance for retrieving context
        """
        self.llm = llm_client or LLMClient()
        self.storage = storage or Storage()

    def generate_response(self, query: str, system_prompt: str,
                         context: Optional[List[Dict]] = None,
                         max_tokens: int = 2000) -> str:
        """
        Generate a response to a query using persona.

        Args:
            query: User query or question
            system_prompt: System prompt with persona characteristics
            context: Optional list of relevant content for context
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response
        """
        # Build the user message with context
        user_message = self._build_user_message(query, context)

        # Generate response
        messages = [{"role": "user", "content": user_message}]

        response = self.llm.generate(
            messages=messages,
            system=system_prompt,
            max_tokens=max_tokens,
            temperature=0.7
        )

        return response

    def _build_user_message(self, query: str, context: Optional[List[Dict]] = None) -> str:
        """
        Build user message with optional context.

        Args:
            query: User query
            context: Optional context items

        Returns:
            Formatted user message
        """
        if not context:
            return query

        # Add relevant context before the query
        context_parts = []
        for i, item in enumerate(context[:3], 1):  # Limit to top 3 items
            content_preview = item.get('content', '')[:1000]  # Limit length
            title = item.get('title', 'Untitled')
            context_parts.append(f"**Reference {i}: {title}**\n{content_preview}")

        context_text = "\n\n".join(context_parts)

        return f"""Use the following references from past communications to inform your response:

{context_text}

---

Now, respond to the following:

{query}"""

    def find_relevant_context(self, query: str, max_items: int = 3) -> List[Dict]:
        """
        Find relevant content from storage based on query.

        Args:
            query: Query to find relevant content for
            max_items: Maximum number of items to return

        Returns:
            List of relevant content items
        """
        # Get all content from storage
        all_content = self.storage.get_all_content()

        if not all_content:
            return []

        # Simple keyword-based relevance (can be improved with embeddings)
        keywords = set(query.lower().split())

        scored_items = []
        for item in all_content:
            content = item.get('content', '').lower()
            # Count keyword matches
            score = sum(1 for kw in keywords if kw in content)
            if score > 0:
                scored_items.append((score, item))

        # Sort by score and return top items
        scored_items.sort(reverse=True, key=lambda x: x[0])
        return [item for _, item in scored_items[:max_items]]

    def generate_fomc_decision(self, economic_data: Dict, system_prompt: str) -> str:
        """
        Generate an FOMC-style decision and statement.

        Args:
            economic_data: Dictionary with economic indicators
            system_prompt: Persona system prompt

        Returns:
            Generated FOMC decision statement
        """
        # Format economic data
        data_text = self._format_economic_data(economic_data)

        query = f"""Based on the following economic data, provide:

1. **Policy Decision**: Should the Federal Reserve raise, lower, or maintain the federal funds rate? By how much?

2. **Rationale**: Explain the reasoning behind this decision, considering:
   - Inflation trends
   - Employment situation
   - Economic growth
   - Financial stability
   - Long-term goals

3. **Forward Guidance**: What signals should be communicated about future policy?

**Current Economic Data:**
{data_text}

Provide your response in the style of an FOMC statement."""

        return self.generate_response(
            query=query,
            system_prompt=system_prompt,
            max_tokens=3000
        )

    def _format_economic_data(self, data: Dict) -> str:
        """Format economic data for the prompt."""
        lines = []
        for key, value in data.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)
