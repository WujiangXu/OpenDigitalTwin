"""English teaching assistant with voice conversation capabilities."""

import os
from typing import Optional, List, Dict
from datetime import datetime

from ..persona.llm_client import LLMClient
from ..memory.digital_twin_memory import DigitalTwinMemory


class EnglishTeacher:
    """An AI-powered English teaching assistant that can converse via voice."""

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        use_memory: bool = True,
        memory_dir: str = "data/teacher_memory"
    ):
        """Initialize the English teaching assistant.

        Args:
            llm_client: LLM client for generating responses
            use_memory: Whether to use memory system to track conversations
            memory_dir: Directory to store conversation memory
        """
        # Initialize LLM client
        if llm_client is None:
            # Use OpenAI by default (since we're using OpenAI for voice)
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            self.llm_client = LLMClient(
                provider="openai",
                api_key=api_key,
                model="gpt-4o",  # Use GPT-4o for best results
                temperature=0.7
            )
        else:
            self.llm_client = llm_client

        # Initialize memory system
        self.use_memory = use_memory
        if use_memory:
            os.makedirs(memory_dir, exist_ok=True)
            self.memory = DigitalTwinMemory(
                memory_dir=memory_dir,
                llm_client=self.llm_client
            )
        else:
            self.memory = None

        # Conversation history (in-memory for current session)
        self.conversation_history: List[Dict[str, str]] = []

        # System prompt for English teaching
        self.system_prompt = """You are a friendly and encouraging English teaching assistant. Your role is to help students practice and improve their English through natural conversation.

Guidelines:
- Be warm, patient, and encouraging
- Speak naturally and conversationally, as if having a real conversation
- Correct mistakes gently by using the correct form in your response, without explicitly pointing out every error
- Ask follow-up questions to keep the conversation flowing
- Adjust your vocabulary and complexity to match the student's level
- Encourage the student to speak more and express themselves
- If asked for grammar explanations, provide clear and simple explanations with examples
- Make learning fun and engaging
- Use varied sentence structures and vocabulary to expose the student to natural English

Remember: Your responses will be converted to speech, so write in a natural, conversational tone. Avoid overly complex sentences or formatting."""

    def chat(self, user_message: str) -> str:
        """Process a user message and generate a teaching response.

        Args:
            user_message: The student's message

        Returns:
            The teacher's response
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })

        # Retrieve relevant context from memory if available
        context = ""
        if self.use_memory and self.memory:
            memories = self.memory.retrieve_relevant_memories(user_message, top_k=3)
            if memories:
                context = "\n\nRelevant previous topics:\n"
                for mem in memories:
                    context += f"- {mem.get('content', '')[:100]}...\n"

        # Build messages for LLM
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        # Add conversation context (last 10 exchanges to keep it manageable)
        recent_history = self.conversation_history[-20:]  # Last 10 exchanges (user + assistant)
        for msg in recent_history:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Generate response
        response = self.llm_client.generate(
            messages=messages,
            temperature=0.7,
            max_tokens=300  # Keep responses concise for voice
        )

        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })

        # Store in memory if enabled
        if self.use_memory and self.memory:
            # Store the exchange
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

        return response

    def get_greeting(self) -> str:
        """Generate a greeting message to start the conversation.

        Returns:
            A friendly greeting
        """
        greetings = [
            "Hello! I'm your English teaching assistant. I'm here to help you practice your English. What would you like to talk about today?",
            "Hi there! Ready to practice some English? Feel free to talk about anything you'd like!",
            "Hey! Great to see you! Let's have a conversation in English. What's on your mind?",
            "Hello! I'm excited to help you practice English today. What topic interests you?",
        ]

        # Use first greeting for first session, vary otherwise
        if len(self.conversation_history) == 0:
            return greetings[0]
        else:
            import random
            return random.choice(greetings[1:])

    def reset_conversation(self):
        """Reset the current conversation history."""
        self.conversation_history = []
        print("✓ Conversation history cleared")

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

        # Generate summary
        summary_prompt = f"""Summarize the main topics discussed in this English learning conversation:

{chr(10).join(user_messages)}

Provide a brief 2-3 sentence summary of what the student talked about."""

        summary = self.llm_client.generate(
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.3,
            max_tokens=150
        )

        return summary

    def save_session(self, filename: Optional[str] = None):
        """Save the conversation history to a file.

        Args:
            filename: Optional filename (defaults to timestamp)
        """
        if not self.conversation_history:
            print("No conversation to save.")
            return

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.txt"

        os.makedirs("data/conversations", exist_ok=True)
        filepath = os.path.join("data/conversations", filename)

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

        print(f"✓ Conversation saved to: {filepath}")
        return filepath
