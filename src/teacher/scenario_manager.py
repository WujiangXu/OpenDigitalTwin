"""Scenario-based conversation manager for English teaching."""

import yaml
import random
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Scenario:
    """Represents a conversation scenario."""

    scenario_id: str
    category: str  # academic, social, professional, everyday, campus_life
    title: str
    description: str
    difficulty: str  # beginner, intermediate, advanced
    duration_minutes: int
    context: str
    ai_role: Dict[str, str]
    learning_objectives: List[str]
    vocabulary_focus: List[str]
    conversation_starters: List[str]
    ai_prompts: Dict[str, Any]

    def get_system_prompt(self) -> str:
        """Generate system prompt for this scenario.

        Returns:
            System prompt configured for the scenario
        """
        prompt = f"""You are participating in a scenario-based English learning conversation.

**Scenario:** {self.title}
**Your Role:** {self.ai_role['name']}
**Personality:** {self.ai_role['personality']}
**Speaking Style:** {self.ai_role['speaking_style']}

**Context:**
{self.context}

**Your Objectives:**
- Stay in character as {self.ai_role['name']}
- Speak naturally as this character would
- Ask relevant follow-up questions
- Provide realistic responses
- Help the student practice natural conversation
- Gently correct major errors by modeling correct usage
- Keep the conversation flowing naturally

**Important:**
- Respond as {self.ai_role['name']} would, not as a teacher
- Don't break character or mention that you're an AI
- Use appropriate vocabulary and tone for this role
- Keep responses conversational (2-4 sentences usually)
- React naturally to what the student says

**Conversation Flow:**
- Start with: "{self.ai_prompts.get('initial', 'Hello!')}"
- Follow up naturally based on student responses
- Use these follow-ups when relevant: {self.ai_prompts.get('follow_up', [])}
"""
        return prompt

    def get_intro_message(self) -> str:
        """Get introduction message for the scenario.

        Returns:
            Formatted introduction
        """
        starters = "\n".join([f"  - {s}" for s in self.conversation_starters])
        objectives = "\n".join([f"  - {obj}" for obj in self.learning_objectives])

        return f"""
📚 **Scenario: {self.title}**
🎯 Difficulty: {self.difficulty} | ⏱️ Duration: ~{self.duration_minutes} minutes

**Situation:**
{self.context}

**You will interact with:** {self.ai_role['name']}
{self.ai_role['personality']}

**Learning Objectives:**
{objectives}

**You can start with:**
{starters}

---
Ready? Start the conversation whenever you're ready!
"""


class ScenarioManager:
    """Manages conversation scenarios for English learning."""

    def __init__(self, scenarios_file: Optional[str] = None):
        """Initialize scenario manager.

        Args:
            scenarios_file: Path to scenarios YAML file.
                          Defaults to cs_phd_scenarios.yaml
        """
        if scenarios_file is None:
            current_dir = Path(__file__).parent
            scenarios_file = current_dir / "scenarios" / "cs_phd_scenarios.yaml"

        self.scenarios_file = Path(scenarios_file)

        if not self.scenarios_file.exists():
            raise FileNotFoundError(
                f"Scenarios file not found: {self.scenarios_file}"
            )

        # Load scenarios
        self._data: Dict[str, Any] = self._load_yaml()
        self._scenarios: Dict[str, Scenario] = self._parse_scenarios()

    def _load_yaml(self) -> Dict[str, Any]:
        """Load scenarios from YAML file.

        Returns:
            Dictionary containing scenario data
        """
        with open(self.scenarios_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _parse_scenarios(self) -> Dict[str, Scenario]:
        """Parse scenarios from YAML data.

        Returns:
            Dictionary mapping scenario_id to Scenario objects
        """
        scenarios = {}

        # Categories to process
        categories = ['academic', 'campus_life', 'social', 'professional', 'everyday']

        for category in categories:
            if category not in self._data:
                continue

            category_data = self._data[category]

            for scenario_key, scenario_data in category_data.items():
                scenario = Scenario(
                    scenario_id=scenario_data['scenario_id'],
                    category=category,
                    title=scenario_data['title'],
                    description=scenario_data['description'],
                    difficulty=scenario_data['difficulty'],
                    duration_minutes=scenario_data['duration_minutes'],
                    context=scenario_data['context'],
                    ai_role=scenario_data['ai_role'],
                    learning_objectives=scenario_data['learning_objectives'],
                    vocabulary_focus=scenario_data['vocabulary_focus'],
                    conversation_starters=scenario_data['conversation_starters'],
                    ai_prompts=scenario_data['ai_prompts']
                )

                scenarios[scenario.scenario_id] = scenario

        return scenarios

    def get_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """Get a specific scenario by ID.

        Args:
            scenario_id: The scenario identifier

        Returns:
            Scenario object or None if not found
        """
        return self._scenarios.get(scenario_id)

    def list_scenarios(
        self,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> List[Scenario]:
        """List available scenarios with optional filters.

        Args:
            category: Filter by category (academic, social, etc.)
            difficulty: Filter by difficulty (beginner, intermediate, advanced)

        Returns:
            List of matching scenarios
        """
        scenarios = list(self._scenarios.values())

        if category:
            scenarios = [s for s in scenarios if s.category == category]

        if difficulty:
            scenarios = [s for s in scenarios if s.difficulty == difficulty]

        return scenarios

    def get_random_scenario(
        self,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> Scenario:
        """Get a random scenario with optional filters.

        Args:
            category: Filter by category
            difficulty: Filter by difficulty

        Returns:
            Random scenario matching criteria
        """
        scenarios = self.list_scenarios(category=category, difficulty=difficulty)

        if not scenarios:
            # Fallback to any scenario
            scenarios = list(self._scenarios.values())

        return random.choice(scenarios)

    def get_recommended_scenarios(self, progress_level: str) -> List[Scenario]:
        """Get recommended scenarios based on student progress.

        Args:
            progress_level: One of: first_week, first_month, first_semester, advanced

        Returns:
            List of recommended scenarios
        """
        if 'progression' not in self._data:
            return []

        progression = self._data['progression']

        if progress_level not in progression:
            return []

        scenario_ids = progression[progress_level].get('recommended_scenarios', [])

        return [
            self._scenarios[sid]
            for sid in scenario_ids
            if sid in self._scenarios
        ]

    def get_categories(self) -> List[str]:
        """Get list of available scenario categories.

        Returns:
            List of category names
        """
        return list(set(s.category for s in self._scenarios.values()))

    def get_cultural_notes(self, topic: Optional[str] = None) -> Dict[str, List[str]]:
        """Get cultural notes for international students.

        Args:
            topic: Specific topic (e.g., 'american_academic_culture')

        Returns:
            Dictionary of cultural notes
        """
        if 'cultural_notes' not in self._data:
            return {}

        notes = self._data['cultural_notes']

        if topic:
            return {topic: notes.get(topic, [])}

        return notes

    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the scenario collection.

        Returns:
            Metadata dictionary
        """
        return self._data.get('metadata', {})

    def search_scenarios(self, keyword: str) -> List[Scenario]:
        """Search scenarios by keyword in title or description.

        Args:
            keyword: Search keyword

        Returns:
            List of matching scenarios
        """
        keyword = keyword.lower()
        results = []

        for scenario in self._scenarios.values():
            if (keyword in scenario.title.lower() or
                keyword in scenario.description.lower() or
                keyword in scenario.context.lower()):
                results.append(scenario)

        return results

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about available scenarios.

        Returns:
            Dictionary with statistics
        """
        scenarios = list(self._scenarios.values())

        return {
            'total_scenarios': len(scenarios),
            'by_category': {
                cat: len([s for s in scenarios if s.category == cat])
                for cat in self.get_categories()
            },
            'by_difficulty': {
                diff: len([s for s in scenarios if s.difficulty == diff])
                for diff in ['beginner', 'intermediate', 'advanced']
            },
            'total_learning_objectives': sum(
                len(s.learning_objectives) for s in scenarios
            ),
            'avg_duration_minutes': sum(
                s.duration_minutes for s in scenarios
            ) / len(scenarios) if scenarios else 0
        }
