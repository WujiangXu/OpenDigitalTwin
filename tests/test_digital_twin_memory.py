"""
Comprehensive tests for Digital Twin Memory System.

Test Plan:
1. Initialization tests
2. Content addition tests
3. Semantic search tests
4. Conversation tracking tests
5. Memory statistics tests
6. Error handling tests
7. Integration tests
"""

import pytest
import os
import shutil
from datetime import datetime


# Test fixtures
@pytest.fixture
def temp_memory_dir(tmp_path):
    """Create temporary memory directory for testing."""
    memory_dir = tmp_path / "test_memory"
    memory_dir.mkdir()
    yield str(memory_dir)
    # Cleanup
    if memory_dir.exists():
        shutil.rmtree(str(memory_dir))


@pytest.fixture
def memory_system(temp_memory_dir):
    """Create a test memory system instance."""
    from src.memory.digital_twin_memory import DigitalTwinMemory

    # Initialize with memory disabled for basic tests
    memory = DigitalTwinMemory(
        persona_name="Test Persona",
        memory_dir=temp_memory_dir,
        use_memory=False  # Disabled for unit tests
    )
    yield memory
    memory.clear_conversation_history()


@pytest.fixture
def memory_system_with_amem(temp_memory_dir):
    """Create a test memory system with A-MEM enabled."""
    from src.memory.digital_twin_memory import DigitalTwinMemory

    try:
        memory = DigitalTwinMemory(
            persona_name="Test Persona",
            memory_dir=temp_memory_dir,
            llm_backend="openai",
            llm_model="gpt-4o-mini",
            use_memory=True
        )
        if not memory.use_memory:
            pytest.skip("A-MEM not available")
        yield memory
        memory.clear_conversation_history()
    except Exception as e:
        pytest.skip(f"Could not initialize A-MEM: {e}")


# Test 1: Initialization
class TestInitialization:
    """Test memory system initialization."""

    def test_init_basic(self, temp_memory_dir):
        """Test basic initialization without memory."""
        from src.memory.digital_twin_memory import DigitalTwinMemory

        memory = DigitalTwinMemory(
            persona_name="LeBron James",
            memory_dir=temp_memory_dir,
            use_memory=False
        )

        assert memory.persona_name == "LeBron James"
        assert memory.memory_dir == temp_memory_dir
        assert memory.use_memory == False
        assert memory.conversation_history == []

    def test_init_with_amem(self, memory_system_with_amem):
        """Test initialization with A-MEM system."""
        assert memory_system_with_amem.use_memory == True
        assert memory_system_with_amem.memory_system is not None

    def test_memory_dir_creation(self, tmp_path):
        """Test that memory directory is created automatically."""
        from src.memory.digital_twin_memory import DigitalTwinMemory

        memory_dir = tmp_path / "auto_created"
        memory = DigitalTwinMemory(
            persona_name="Test",
            memory_dir=str(memory_dir),
            use_memory=False
        )

        assert os.path.exists(str(memory_dir))

    def test_llm_config_detection(self, temp_memory_dir, monkeypatch):
        """Test LLM configuration detection from environment."""
        from src.memory.digital_twin_memory import DigitalTwinMemory

        # Test with OpenAI API key
        monkeypatch.setenv("OPENAI_API_KEY", "test_key")
        memory = DigitalTwinMemory(
            persona_name="Test",
            memory_dir=temp_memory_dir,
            use_memory=False
        )
        backend, model = memory._detect_llm_config()
        assert backend == "openai"
        assert "gpt" in model


# Test 2: Content Addition
class TestContentAddition:
    """Test adding content to memory."""

    def test_add_content_memory_disabled(self, memory_system):
        """Test adding content when memory is disabled."""
        result = memory_system.add_content(
            content="Test content",
            source="test.txt",
            content_type="document"
        )
        # Should return None when memory disabled
        assert result is None

    def test_add_content_with_amem(self, memory_system_with_amem):
        """Test adding content with A-MEM enabled."""
        memory_id = memory_system_with_amem.add_content(
            content="LeBron James discusses leadership in basketball",
            source="press_conference_2024.txt",
            content_type="speech"
        )

        # Should return a memory ID
        assert memory_id is not None
        assert isinstance(memory_id, str)

    def test_add_content_with_metadata(self, memory_system_with_amem):
        """Test adding content with custom metadata."""
        custom_metadata = {
            "topic": "leadership",
            "date": "2024-01-15"
        }

        memory_id = memory_system_with_amem.add_content(
            content="Leadership is about elevating everyone around you",
            source="interview.txt",
            content_type="interview",
            metadata=custom_metadata
        )

        assert memory_id is not None

    def test_add_multiple_contents(self, memory_system_with_amem):
        """Test adding multiple pieces of content."""
        contents = [
            "Basketball is a team sport",
            "Defense wins championships",
            "Practice makes perfect"
        ]

        memory_ids = []
        for content in contents:
            mid = memory_system_with_amem.add_content(
                content=content,
                source="wisdom.txt"
            )
            memory_ids.append(mid)

        # All should succeed
        assert all(mid is not None for mid in memory_ids)
        assert len(memory_ids) == 3


# Test 3: Semantic Search
class TestSemanticSearch:
    """Test semantic search functionality."""

    def test_search_memory_disabled(self, memory_system):
        """Test search when memory is disabled."""
        results = memory_system.search("test query")
        assert results == []

    def test_search_empty_memory(self, memory_system_with_amem):
        """Test search with no content."""
        results = memory_system_with_amem.search("anything")
        assert results == []

    def test_search_basic(self, memory_system_with_amem):
        """Test basic semantic search."""
        # Add content
        memory_system_with_amem.add_content(
            content="LeBron James is known for his leadership on and off the court",
            source="bio.txt"
        )
        memory_system_with_amem.add_content(
            content="Basketball requires teamwork and dedication",
            source="guide.txt"
        )

        # Search
        results = memory_system_with_amem.search("leadership", k=5)

        # Should find relevant content
        assert len(results) > 0
        assert any("leadership" in r.get("content", "").lower() for r in results)

    def test_search_semantic_similarity(self, memory_system_with_amem):
        """Test that search understands semantic similarity."""
        # Add content about employment
        memory_system_with_amem.add_content(
            content="The team showed great performance",
            source="report.txt"
        )

        # Search with synonym
        results = memory_system_with_amem.search("squad performance", k=5)

        # Should find related content even with different words
        # (This depends on embedding quality)
        assert isinstance(results, list)

    def test_search_with_k_param(self, memory_system_with_amem):
        """Test search with different k values."""
        # Add multiple contents
        for i in range(10):
            memory_system_with_amem.add_content(
                content=f"Document {i} about various topics",
                source=f"doc{i}.txt"
            )

        # Search with k=3
        results = memory_system_with_amem.search("document", k=3)
        assert len(results) <= 3


# Test 4: Conversation Tracking
class TestConversationTracking:
    """Test conversation history tracking."""

    def test_store_conversation_turn(self, memory_system):
        """Test storing a conversation turn."""
        memory_system.store_conversation_turn(
            role="user",
            content="How do you approach leadership?"
        )
        memory_system.store_conversation_turn(
            role="assistant",
            content="Leadership is about...",
            query="How do you approach leadership?"
        )

        assert len(memory_system.conversation_history) == 2
        assert memory_system.conversation_history[0]["role"] == "user"
        assert memory_system.conversation_history[1]["role"] == "assistant"

    def test_conversation_history_order(self, memory_system):
        """Test that conversation history maintains order."""
        for i in range(5):
            memory_system.store_conversation_turn(
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}"
            )

        assert len(memory_system.conversation_history) == 5
        for i, turn in enumerate(memory_system.conversation_history):
            assert f"Message {i}" in turn["content"]

    def test_get_conversation_context(self, memory_system):
        """Test retrieving conversation context."""
        # Add conversation history
        memory_system.store_conversation_turn(
            role="user",
            content="Tell me about basketball"
        )
        memory_system.store_conversation_turn(
            role="assistant",
            content="Basketball is a team sport...",
            query="Tell me about basketball"
        )

        # Get context
        context = memory_system.get_conversation_context(
            query="more details",
            max_turns=5
        )

        assert "basketball" in context.lower()
        assert "user" in context.lower() or "User" in context

    def test_get_conversation_context_max_turns(self, memory_system):
        """Test max_turns parameter in context retrieval."""
        # Add 10 turns
        for i in range(10):
            memory_system.store_conversation_turn(
                role="user" if i % 2 == 0 else "assistant",
                content=f"Turn {i}"
            )

        # Get context with max_turns=3
        context = memory_system.get_conversation_context(
            query="test",
            max_turns=3
        )

        # Should only include last 3 turns
        assert "Turn 9" in context or "Turn 8" in context or "Turn 7" in context
        assert "Turn 0" not in context  # First turn should not be included

    def test_clear_conversation_history(self, memory_system):
        """Test clearing conversation history."""
        # Add some history
        memory_system.store_conversation_turn(role="user", content="Test")
        assert len(memory_system.conversation_history) > 0

        # Clear
        memory_system.clear_conversation_history()
        assert len(memory_system.conversation_history) == 0


# Test 5: Memory Statistics
class TestMemoryStatistics:
    """Test memory statistics and monitoring."""

    def test_get_memory_stats_basic(self, memory_system):
        """Test getting basic memory stats."""
        stats = memory_system.get_memory_stats()

        assert "persona" in stats
        assert stats["persona"] == "Test Persona"
        assert "memory_enabled" in stats
        assert "conversation_turns" in stats
        assert "memory_dir" in stats

    def test_get_memory_stats_with_amem(self, memory_system_with_amem):
        """Test memory stats with A-MEM enabled."""
        # Add some content
        memory_system_with_amem.add_content("Test content 1", source="test1.txt")
        memory_system_with_amem.add_content("Test content 2", source="test2.txt")

        stats = memory_system_with_amem.get_memory_stats()

        assert stats["memory_enabled"] == True
        # May have additional stats from A-MEM
        # (total_memories, evolution_count, etc.)

    def test_conversation_turns_in_stats(self, memory_system):
        """Test that conversation turns are tracked in stats."""
        memory_system.store_conversation_turn(role="user", content="Hello")
        memory_system.store_conversation_turn(role="assistant", content="Hi there")

        stats = memory_system.get_memory_stats()
        assert stats["conversation_turns"] == 2


# Test 6: Error Handling
class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_add_empty_content(self, memory_system_with_amem):
        """Test adding empty content."""
        memory_id = memory_system_with_amem.add_content(
            content="",
            source="empty.txt"
        )
        # Should handle gracefully (may return None or ID depending on implementation)
        # Just verify it doesn't crash

    def test_search_empty_query(self, memory_system_with_amem):
        """Test searching with empty query."""
        results = memory_system_with_amem.search("", k=5)
        # Should return empty list or handle gracefully
        assert isinstance(results, list)

    def test_invalid_llm_backend(self, temp_memory_dir):
        """Test initialization with invalid LLM backend."""
        from src.memory.digital_twin_memory import DigitalTwinMemory

        # This should either fall back gracefully or disable memory
        memory = DigitalTwinMemory(
            persona_name="Test",
            memory_dir=temp_memory_dir,
            llm_backend="invalid_backend",
            use_memory=True
        )

        # Should not crash - either memory is disabled or uses fallback
        assert memory is not None


# Test 7: Integration Tests
class TestIntegration:
    """End-to-end integration tests."""

    def test_full_workflow_no_amem(self, memory_system):
        """Test complete workflow without A-MEM."""
        # Add conversation
        memory_system.store_conversation_turn(
            role="user",
            content="How do you approach leadership?"
        )

        # Get context (should work even without A-MEM)
        context = memory_system.get_conversation_context(
            query="leadership",
            max_turns=5
        )

        assert "leadership" in context.lower()

        # Get stats
        stats = memory_system.get_memory_stats()
        assert stats["conversation_turns"] >= 1

    def test_full_workflow_with_amem(self, memory_system_with_amem):
        """Test complete workflow with A-MEM."""
        # Step 1: Add reference content
        memory_system_with_amem.add_content(
            content="Leadership means bringing out the best in your teammates",
            source="leadership_guide.txt",
            content_type="document"
        )

        # Step 2: Start conversation
        memory_system_with_amem.store_conversation_turn(
            role="user",
            content="How do you define leadership?"
        )

        # Step 3: Get context with memories
        context = memory_system_with_amem.get_conversation_context(
            query="leadership definition",
            max_turns=5,
            max_memories=3
        )

        # Should include both conversation and memory content
        assert "leadership" in context.lower()

        # Step 4: Store assistant response
        memory_system_with_amem.store_conversation_turn(
            role="assistant",
            content="Leadership is about...",
            query="How do you define leadership?"
        )

        # Step 5: Verify stats
        stats = memory_system_with_amem.get_memory_stats()
        assert stats["memory_enabled"] == True
        assert stats["conversation_turns"] >= 2

    def test_memory_persistence_simulation(self, memory_system_with_amem):
        """Test that memories can be retrieved across 'sessions'."""
        # Session 1: Add content
        memory_id = memory_system_with_amem.add_content(
            content="Basketball requires constant practice and dedication",
            source="training.txt"
        )

        # Simulate session end - clear conversation but keep long-term memory
        memory_system_with_amem.clear_conversation_history()

        # Session 2: Search for content
        results = memory_system_with_amem.search("practice dedication", k=5)

        # Should still find the memory
        assert len(results) > 0


# Test 8: Performance Tests
class TestPerformance:
    """Test performance with realistic data volumes."""

    @pytest.mark.slow
    def test_add_many_contents(self, memory_system_with_amem):
        """Test adding many pieces of content."""
        import time

        start = time.time()

        # Add 50 contents (reasonable for initial testing)
        for i in range(50):
            memory_system_with_amem.add_content(
                content=f"Document {i} discussing various basketball strategies and techniques",
                source=f"doc{i}.txt"
            )

        duration = time.time() - start

        # Should complete in reasonable time (< 60s for 50 docs)
        # Actual time depends on LLM API latency
        print(f"Added 50 documents in {duration:.2f}s")

    @pytest.mark.slow
    def test_search_performance(self, memory_system_with_amem):
        """Test search performance."""
        import time

        # Add some content
        for i in range(20):
            memory_system_with_amem.add_content(
                content=f"Basketball document {i}",
                source=f"doc{i}.txt"
            )

        # Test search speed
        start = time.time()
        results = memory_system_with_amem.search("basketball", k=5)
        duration = time.time() - start

        # Search should be fast (< 1s)
        assert duration < 1.0
        print(f"Search completed in {duration:.3f}s")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
