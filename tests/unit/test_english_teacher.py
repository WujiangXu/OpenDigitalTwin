"""Unit tests for EnglishTeacher (refactored version)."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.teacher.english_teacher import EnglishTeacher
from src.teacher.config import TeacherConfig
from src.teacher.prompt_loader import PromptLoader


class MockLLMClient:
    """Mock LLM client for testing."""

    def __init__(self, *args, **kwargs):
        """Initialize mock client."""
        self.generate_calls = []

    def generate(self, messages, temperature=0.7, max_tokens=300):
        """Mock generate method.

        Args:
            messages: List of messages
            temperature: Temperature parameter
            max_tokens: Max tokens parameter

        Returns:
            Mock response string
        """
        self.generate_calls.append({
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        })
        return "This is a mock response from the teacher."


class TestEnglishTeacher:
    """Test cases for EnglishTeacher class."""

    @pytest.fixture
    def mock_llm_client(self):
        """Create a mock LLM client."""
        return MockLLMClient()

    @pytest.fixture
    def teacher_config(self, temp_dir):
        """Create a test configuration."""
        return TeacherConfig(
            use_memory=False,  # Disable memory for simpler tests
            memory_dir=f"{temp_dir}/memory",
            conversation_dir=f"{temp_dir}/conversations"
        )

    @pytest.fixture
    def teacher(self, mock_llm_client, teacher_config, prompts_file):
        """Create an EnglishTeacher instance for testing."""
        prompt_loader = PromptLoader(prompts_file)
        return EnglishTeacher(
            llm_client=mock_llm_client,
            config=teacher_config,
            prompt_loader=prompt_loader
        )

    def test_initialization(self, teacher, teacher_config):
        """Test teacher initialization."""
        assert teacher.config == teacher_config
        assert teacher.system_prompt is not None
        assert len(teacher.conversation_history) == 0

    def test_initialization_without_api_key(self, teacher_config, prompts_file, monkeypatch):
        """Test initialization fails without API key."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        prompt_loader = PromptLoader(prompts_file)
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            EnglishTeacher(
                config=teacher_config,
                prompt_loader=prompt_loader
            )

    def test_chat_success(self, teacher):
        """Test successful chat interaction."""
        response = teacher.chat("Hello, I want to learn English")

        assert response == "This is a mock response from the teacher."
        assert len(teacher.conversation_history) == 2  # User + assistant
        assert teacher.conversation_history[0]["role"] == "user"
        assert teacher.conversation_history[1]["role"] == "assistant"

    def test_chat_empty_message(self, teacher):
        """Test chat with empty message."""
        with pytest.raises(ValueError, match="cannot be empty"):
            teacher.chat("")

    def test_chat_whitespace_only_message(self, teacher):
        """Test chat with whitespace-only message."""
        with pytest.raises(ValueError, match="cannot be empty"):
            teacher.chat("   ")

    def test_chat_multiple_exchanges(self, teacher):
        """Test multiple chat exchanges."""
        teacher.chat("Hello")
        teacher.chat("How are you?")
        teacher.chat("Tell me about grammar")

        assert len(teacher.conversation_history) == 6  # 3 exchanges × 2 messages

    def test_get_greeting_first_time(self, teacher):
        """Test getting greeting for first conversation."""
        greeting = teacher.get_greeting()
        assert greeting == "Hello test!"  # First greeting from test prompts

    def test_get_greeting_subsequent(self, teacher):
        """Test getting greeting after conversation started."""
        # Add some conversation history
        teacher.conversation_history.append({
            "role": "user",
            "content": "test",
            "timestamp": "2025-01-15"
        })

        greeting = teacher.get_greeting()
        # Should be one of the other greetings, not the first
        assert greeting in ["Hi there test!", "Welcome test!"]

    def test_reset_conversation(self, teacher):
        """Test conversation reset."""
        teacher.chat("Test message")
        assert len(teacher.conversation_history) > 0

        teacher.reset_conversation()
        assert len(teacher.conversation_history) == 0

    def test_get_conversation_summary(self, teacher):
        """Test getting conversation summary."""
        teacher.chat("I want to talk about travel")
        teacher.chat("What's your favorite destination?")

        summary = teacher.get_conversation_summary()
        assert isinstance(summary, str)
        assert len(summary) > 0

    def test_get_conversation_summary_empty(self, teacher):
        """Test getting summary with no conversation."""
        summary = teacher.get_conversation_summary()
        assert summary == "No conversation yet."

    def test_save_session_success(self, teacher, temp_dir):
        """Test successful session save."""
        teacher.chat("Test conversation")

        filepath = teacher.save_session()

        assert filepath is not None
        assert filepath.endswith(".txt")

        # Verify file exists and has content
        with open(filepath, 'r') as f:
            content = f.read()
            assert "English Teaching Session" in content
            assert "Test conversation" in content

    def test_save_session_empty_conversation(self, teacher):
        """Test saving with empty conversation."""
        filepath = teacher.save_session()
        assert filepath is None

    def test_save_session_custom_filename(self, teacher):
        """Test saving with custom filename."""
        teacher.chat("Test")

        filepath = teacher.save_session("custom_session.txt")

        assert filepath is not None
        assert "custom_session.txt" in filepath

    def test_get_stats(self, teacher):
        """Test getting session statistics."""
        teacher.chat("Hello, I want to practice")
        teacher.chat("Tell me about grammar")

        stats = teacher.get_stats()

        assert stats["total_exchanges"] == 2
        assert stats["student_words"] > 0
        assert stats["teacher_words"] > 0
        assert "model" in stats
        assert "memory_enabled" in stats

    def test_get_stats_empty(self, teacher):
        """Test stats with empty conversation."""
        stats = teacher.get_stats()

        assert stats["total_exchanges"] == 0
        assert stats["student_words"] == 0
        assert stats["teacher_words"] == 0

    def test_build_llm_messages(self, teacher):
        """Test building messages for LLM API."""
        teacher.chat("First message")
        teacher.chat("Second message")

        messages = teacher._build_llm_messages("")

        # Should have system message + conversation history
        assert len(messages) > 0
        assert messages[0]["role"] == "system"

    def test_conversation_history_limit(self, teacher):
        """Test that conversation history is limited in LLM context."""
        # Add many messages
        for i in range(15):
            teacher.chat(f"Message {i}")

        messages = teacher._build_llm_messages("")

        # Should not include all messages (limited by max_history_exchanges)
        # System + limited history
        max_messages = 1 + (teacher.config.max_history_exchanges * 2)
        assert len(messages) <= max_messages


class TestEnglishTeacherWithMemory:
    """Test cases for EnglishTeacher with memory enabled."""

    @pytest.fixture
    def teacher_with_memory(self, mock_llm_client, temp_dir, prompts_file):
        """Create teacher with memory enabled."""
        config = TeacherConfig(
            use_memory=True,
            memory_dir=f"{temp_dir}/memory",
            conversation_dir=f"{temp_dir}/conversations"
        )
        prompt_loader = PromptLoader(prompts_file)

        # Mock the memory system since we don't want to initialize ChromaDB in tests
        with patch('src.teacher.english_teacher.DigitalTwinMemory'):
            teacher = EnglishTeacher(
                llm_client=mock_llm_client,
                config=config,
                prompt_loader=prompt_loader
            )
            # Set mock memory
            teacher.memory = Mock()
            teacher.memory.retrieve_relevant_memories.return_value = []
            teacher.memory.add_memory = Mock()

            return teacher

    def test_chat_with_memory_storage(self, teacher_with_memory):
        """Test that conversations are stored in memory."""
        teacher_with_memory.chat("Test message")

        # Verify memory.add_memory was called
        assert teacher_with_memory.memory.add_memory.called

    def test_memory_retrieval(self, teacher_with_memory):
        """Test memory retrieval during chat."""
        # Mock memory retrieval
        teacher_with_memory.memory.retrieve_relevant_memories.return_value = [
            {"content": "Previous topic about grammar"}
        ]

        teacher_with_memory.chat("Tell me more about that")

        # Verify memory was queried
        assert teacher_with_memory.memory.retrieve_relevant_memories.called
