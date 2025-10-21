"""
Persona analyzer that uses LLM to extract patterns and characteristics.
"""
from typing import List, Dict
import json
from .llm_client import LLMClient


class PersonaAnalyzer:
    """Analyzes content to build a persona profile using LLM."""

    def __init__(self, llm_client: LLMClient = None):
        """
        Initialize persona analyzer.

        Args:
            llm_client: LLM client instance
        """
        self.llm = llm_client or LLMClient()

    def analyze_content(self, content_items: List[Dict]) -> Dict:
        """
        Analyze content to extract persona characteristics.

        Args:
            content_items: List of content dictionaries with 'content' key

        Returns:
            Persona profile dictionary
        """
        # Combine content for analysis
        combined_text = self._prepare_content(content_items)

        # Analyze different aspects
        print("Analyzing writing style...")
        writing_style = self._analyze_writing_style(combined_text)

        print("Analyzing communication patterns...")
        communication_patterns = self._analyze_communication_patterns(combined_text)

        print("Analyzing key topics and themes...")
        topics_themes = self._analyze_topics(combined_text)

        print("Analyzing decision-making approach...")
        decision_style = self._analyze_decision_style(combined_text)

        # Compile persona profile
        persona = {
            'writing_style': writing_style,
            'communication_patterns': communication_patterns,
            'topics_themes': topics_themes,
            'decision_style': decision_style,
            'content_count': len(content_items)
        }

        return persona

    def _prepare_content(self, content_items: List[Dict], max_length: int = 50000) -> str:
        """Prepare and combine content for analysis."""
        texts = []
        total_length = 0

        for item in content_items:
            content = item.get('content', '')
            if content:
                texts.append(content)
                total_length += len(content)

                # Limit total length to avoid token limits
                if total_length > max_length:
                    break

        return "\n\n---\n\n".join(texts)[:max_length]

    def _analyze_writing_style(self, text: str) -> str:
        """Analyze writing style characteristics."""
        prompt = """Analyze the writing style of the following text. Focus on:
1. Tone (formal, conversational, technical, etc.)
2. Sentence structure (short/long, simple/complex)
3. Vocabulary level and word choice
4. Common phrases or expressions
5. Use of data, evidence, or examples

Provide a concise summary (3-5 sentences) of the writing style."""

        return self.llm.analyze_text(text[:15000], prompt)

    def _analyze_communication_patterns(self, text: str) -> str:
        """Analyze communication patterns."""
        prompt = """Analyze the communication patterns in the following text. Focus on:
1. How ideas are structured and presented
2. Use of analogies, metaphors, or examples
3. Level of directness vs. diplomatic language
4. Emphasis on certain topics or themes
5. How uncertainty or confidence is expressed

Provide a concise summary (3-5 sentences) of the communication patterns."""

        return self.llm.analyze_text(text[:15000], prompt)

    def _analyze_topics(self, text: str) -> str:
        """Analyze key topics and themes."""
        prompt = """Identify and analyze the key topics and themes in the following text. Focus on:
1. Main topics frequently discussed
2. Recurring themes or concerns
3. Areas of expertise or focus
4. How different topics are connected

Provide a concise summary (3-5 sentences) of the main topics and themes."""

        return self.llm.analyze_text(text[:15000], prompt)

    def _analyze_decision_style(self, text: str) -> str:
        """Analyze decision-making style."""
        prompt = """Analyze the decision-making approach in the following text. Focus on:
1. How decisions are framed and justified
2. Use of data vs. judgment
3. Consideration of risks and uncertainties
4. Balance between different factors or stakeholders
5. Communication of decisions and rationale

Provide a concise summary (3-5 sentences) of the decision-making style."""

        return self.llm.analyze_text(text[:15000], prompt)

    def create_system_prompt(self, persona: Dict, person_name: str = "this person") -> str:
        """
        Create a system prompt for the LLM based on persona analysis.

        Args:
            persona: Persona profile dictionary
            person_name: Name of the person to emulate

        Returns:
            System prompt string
        """
        system_prompt = f"""You are a digital twin of {person_name}. Your goal is to respond and make decisions in the same style and manner as {person_name}.

**Writing Style:**
{persona.get('writing_style', 'Not available')}

**Communication Patterns:**
{persona.get('communication_patterns', 'Not available')}

**Key Topics and Themes:**
{persona.get('topics_themes', 'Not available')}

**Decision-Making Approach:**
{persona.get('decision_style', 'Not available')}

When responding:
- Maintain {person_name}'s tone, style, and communication patterns
- Use similar language, phrases, and vocabulary
- Consider topics and themes in the same way {person_name} would
- Apply the same decision-making approach
- Be authentic to {person_name}'s perspective and reasoning

Base your responses on the patterns observed in {person_name}'s actual communications and writings."""

        return system_prompt
