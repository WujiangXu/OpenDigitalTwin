"""English teaching assistant with voice conversation capabilities (refactored)."""

import os
import logging
import random
from typing import Optional, List, Dict
from datetime import datetime
from pathlib import Path

from ..persona.llm_client import LLMClient
from ..memory.digital_twin_memory import DigitalTwinMemory
from .prompt_loader import PromptLoader
from .config import TeacherConfig
from .scenario_manager import ScenarioManager, Scenario


# Configure logging
logger = logging.getLogger(__name__)


class EnglishTeacher:
    """An AI-powered English teaching assistant that can converse via voice."""

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        config: Optional[TeacherConfig] = None,
        prompt_loader: Optional[PromptLoader] = None,
        scenario_manager: Optional[ScenarioManager] = None
    ):
        """Initialize the English teaching assistant.

        Args:
            llm_client: LLM client for generating responses
            config: Configuration object for the teacher
            prompt_loader: Prompt template loader
            scenario_manager: Scenario manager for role-play conversations
        """
        # Initialize configuration
        self.config = config or TeacherConfig.from_env()
        logger.info(f"Initializing EnglishTeacher with config: {self.config}")

        # Initialize prompt loader
        self.prompt_loader = prompt_loader or PromptLoader()

        # Initialize LLM client
        if llm_client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")

            self.llm_client = LLMClient(
                provider="openai",
                api_key=api_key,
                model=self.config.model,
                temperature=self.config.temperature
            )
            logger.info(f"Created LLM client with model: {self.config.model}")
        else:
            self.llm_client = llm_client

        # Initialize memory system
        self.memory: Optional[DigitalTwinMemory] = None
        if self.config.use_memory:
            try:
                os.makedirs(self.config.memory_dir, exist_ok=True)
                self.memory = DigitalTwinMemory(
                    memory_dir=self.config.memory_dir,
                    llm_client=self.llm_client
                )
                logger.info(f"Memory system enabled at: {self.config.memory_dir}")
            except Exception as e:
                logger.warning(f"Failed to initialize memory system: {e}")
                self.memory = None

        # Conversation history (in-memory for current session)
        self.conversation_history: List[Dict[str, str]] = []

        # Scenario management
        self.scenario_manager = scenario_manager or ScenarioManager()
        self.current_scenario: Optional[Scenario] = None

        # Load system prompt
        self.system_prompt = self.prompt_loader.get_system_prompt()

    def chat(self, user_message: str) -> str:
        """Process a user message and generate a teaching response.

        Args:
            user_message: The student's message

        Returns:
            The teacher's response

        Raises:
            ValueError: If user_message is empty
            Exception: If response generation fails
        """
        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty")

        logger.info(f"Processing user message: {user_message[:100]}...")

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })

        try:
            # Retrieve relevant context from memory if available
            context = self._get_memory_context(user_message)

            # Build messages for LLM
            messages = self._build_llm_messages(context)

            # Generate response
            response = self.llm_client.generate(
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )

            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })

            # Store in memory if enabled
            if self.config.use_memory and self.memory:
                self._store_exchange_in_memory(user_message, response)

            logger.info(f"Generated response: {response[:100]}...")
            return response

        except Exception as e:
            logger.error(f"Error generating response: {e}", exc_info=True)
            raise Exception(f"Failed to generate response: {str(e)}")

    def _get_memory_context(self, user_message: str) -> str:
        """Retrieve relevant context from memory.

        Args:
            user_message: The user's current message

        Returns:
            Context string from memory
        """
        context = ""
        if self.memory:
            try:
                memories = self.memory.retrieve_relevant_memories(
                    user_message,
                    top_k=self.config.memory_retrieval_top_k
                )
                if memories:
                    context = "\n\nRelevant previous topics:\n"
                    for mem in memories:
                        content = mem.get('content', '')[:100]
                        context += f"- {content}...\n"
                    logger.debug(f"Retrieved {len(memories)} memories")
            except Exception as e:
                logger.warning(f"Failed to retrieve memories: {e}")

        return context

    def _build_llm_messages(self, context: str) -> List[Dict[str, str]]:
        """Build message list for LLM API call.

        Args:
            context: Additional context from memory

        Returns:
            List of message dictionaries
        """
        messages = [
            {"role": "system", "content": self.system_prompt + context}
        ]

        # Add recent conversation history
        max_exchanges = self.config.max_history_exchanges * 2  # user + assistant
        recent_history = self.conversation_history[-max_exchanges:]

        for msg in recent_history:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        return messages

    def _store_exchange_in_memory(self, user_message: str, response: str):
        """Store conversation exchange in memory.

        Args:
            user_message: The user's message
            response: The assistant's response
        """
        try:
            exchange = f"Student: {user_message}\nTeacher: {response}"
            self.memory.add_memory(
                content=exchange,
                metadata={
                    "type": "conversation",
                    "student_message": user_message,
                    "teacher_response": response,
                    "timestamp": datetime.now().isoformat()
                }
            )
            logger.debug("Stored exchange in memory")
        except Exception as e:
            logger.warning(f"Failed to store exchange in memory: {e}")

    def get_greeting(self) -> str:
        """Generate a greeting message to start the conversation.

        Returns:
            A friendly greeting
        """
        greetings = self.prompt_loader.load_greetings()

        # Use first greeting for first session, vary otherwise
        if len(self.conversation_history) == 0:
            return greetings[0]
        else:
            return random.choice(greetings[1:])

    def reset_conversation(self):
        """Reset the current conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation.

        Returns:
            Summary of topics discussed
        """
        if not self.conversation_history:
            return "No conversation yet."

        # Extract user messages
        user_messages = [
            msg["content"] for msg in self.conversation_history
            if msg["role"] == "user"
        ]

        if not user_messages:
            return "No conversation yet."

        try:
            # Build conversation text
            conversation_text = "\n".join(user_messages)

            # Get summary prompt
            summary_prompt = self.prompt_loader.get_summary_prompt(
                conversation_text
            )

            # Generate summary
            summary = self.llm_client.generate(
                messages=[{"role": "user", "content": summary_prompt}],
                temperature=0.3,
                max_tokens=150
            )

            logger.info("Generated conversation summary")
            return summary

        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return "Summary generation failed."

    def save_session(self, filename: Optional[str] = None) -> Optional[str]:
        """Save the conversation history to a file.

        Args:
            filename: Optional filename (defaults to timestamp)

        Returns:
            Path to saved file, or None if save failed
        """
        if not self.conversation_history:
            logger.warning("No conversation to save")
            return None

        try:
            # Generate filename if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"conversation_{timestamp}.txt"

            # Ensure conversation directory exists
            os.makedirs(self.config.conversation_dir, exist_ok=True)
            filepath = os.path.join(self.config.conversation_dir, filename)

            # Write conversation to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("=" * 50 + "\n")
                f.write("English Teaching Session\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")

                for msg in self.conversation_history:
                    role = "Student" if msg["role"] == "user" else "Teacher"
                    f.write(f"{role}: {msg['content']}\n\n")

                # Add summary
                f.write("\n" + "=" * 50 + "\n")
                f.write("Session Summary:\n")
                f.write(self.get_conversation_summary() + "\n")

            logger.info(f"Conversation saved to: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to save conversation: {e}", exc_info=True)
            return None

    def get_stats(self) -> Dict[str, any]:
        """Get statistics about the current session.

        Returns:
            Dictionary with session statistics
        """
        user_messages = [
            msg for msg in self.conversation_history
            if msg["role"] == "user"
        ]
        teacher_messages = [
            msg for msg in self.conversation_history
            if msg["role"] == "assistant"
        ]

        return {
            "total_exchanges": len(user_messages),
            "student_words": sum(len(msg["content"].split()) for msg in user_messages),
            "teacher_words": sum(len(msg["content"].split()) for msg in teacher_messages),
            "memory_enabled": self.config.use_memory,
            "model": self.config.model
        }

    # Scenario-based learning methods
   
    def start_scenario(self, scenario_id: str) -> str:
        """Start a scenario-based conversation.

        Args:
            scenario_id: ID of the scenario to start

        Returns:
            Introduction message for the scenario
        """
        scenario = self.scenario_manager.get_scenario(scenario_id)
        
        if not scenario:
            raise ValueError(f"Scenario not found: {scenario_id}")
        
        # Reset conversation for new scenario
        self.reset_conversation()
        
        # Set current scenario
        self.current_scenario = scenario
        
        # Override system prompt with scenario-specific one
        self.system_prompt = scenario.get_system_prompt()
        
        logger.info(f"Started scenario: {scenario.title}")
        
        return scenario.get_intro_message()
    
    def is_in_scenario(self) -> bool:
        """Check if currently in a scenario.

        Returns:
            True if in scenario mode
        """
        return self.current_scenario is not None
    
    def end_scenario(self) -> Dict[str, Any]:
        """End the current scenario and get summary.

        Returns:
            Dictionary with scenario summary and statistics
        """
        if not self.current_scenario:
            return {"error": "No active scenario"}
        
        summary = {
            "scenario": self.current_scenario.title,
            "duration": len(self.conversation_history) // 2,  # Number of exchanges
            "vocabulary_practiced": self.current_scenario.vocabulary_focus,
            "learning_objectives": self.current_scenario.learning_objectives,
            "conversation_summary": self.get_conversation_summary()
        }
        
        # Reset to normal mode
        self.current_scenario = None
        self.system_prompt = self.prompt_loader.get_system_prompt()
        
        logger.info(f"Ended scenario: {summary['scenario']}")
        
        return summary
    
    def get_scenario_progress(self) -> Optional[Dict[str, Any]]:
        """Get progress information for current scenario.

        Returns:
            Progress dictionary or None if not in scenario
        """
        if not self.current_scenario:
            return None
        
        exchanges = len(self.conversation_history) // 2
        estimated_duration = self.current_scenario.duration_minutes
        
        return {
            "scenario": self.current_scenario.title,
            "exchanges_completed": exchanges,
            "estimated_duration_minutes": estimated_duration,
            "vocabulary_focus": self.current_scenario.vocabulary_focus,
            "ai_character": self.current_scenario.ai_role['name']
        }
