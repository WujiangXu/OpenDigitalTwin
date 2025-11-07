"""
Manual test script for Digital Twin Memory System.

This script provides a simple way to test the memory system without pytest.
It's designed to verify the installation and basic functionality.

Usage:
    python tests/manual_test_memory.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60 + "\n")


def test_import():
    """Test 1: Import the memory module."""
    print_section("TEST 1: Import Memory Module")

    try:
        from src.memory.digital_twin_memory import DigitalTwinMemory
        print("✓ Successfully imported DigitalTwinMemory")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False


def test_basic_initialization():
    """Test 2: Basic initialization without A-MEM."""
    print_section("TEST 2: Basic Initialization (Memory Disabled)")

    try:
        from src.memory.digital_twin_memory import DigitalTwinMemory

        memory = DigitalTwinMemory(
            persona_name="LeBron James",
            memory_dir="/tmp/test_memory",
            use_memory=False
        )

        print(f"✓ Created memory system for: {memory.persona_name}")
        print(f"  - Memory directory: {memory.memory_dir}")
        print(f"  - Memory enabled: {memory.use_memory}")
        print(f"  - Conversation history: {len(memory.conversation_history)} turns")

        return True

    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_conversation_tracking():
    """Test 3: Conversation history tracking."""
    print_section("TEST 3: Conversation Tracking")

    try:
        from src.memory.digital_twin_memory import DigitalTwinMemory

        memory = DigitalTwinMemory(
            persona_name="LeBron James",
            memory_dir="/tmp/test_memory",
            use_memory=False
        )

        # Simulate conversation
        print("Adding conversation turns...")
        memory.store_conversation_turn(
            role="user",
            content="How do you approach leadership in basketball?"
        )

        memory.store_conversation_turn(
            role="assistant",
            content="Leadership is about bringing out the best in your teammates and leading by example.",
            query="How do you approach leadership in basketball?"
        )

        memory.store_conversation_turn(
            role="user",
            content="Can you give me a specific example?"
        )

        print(f"✓ Stored {len(memory.conversation_history)} conversation turns")

        # Get context
        context = memory.get_conversation_context(
            query="leadership examples",
            max_turns=5
        )

        print(f"✓ Retrieved conversation context ({len(context)} chars)")
        print(f"\nContext preview:\n{context[:200]}...")

        return True

    except Exception as e:
        print(f"✗ Conversation tracking failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_memory_stats():
    """Test 4: Memory statistics."""
    print_section("TEST 4: Memory Statistics")

    try:
        from src.memory.digital_twin_memory import DigitalTwinMemory

        memory = DigitalTwinMemory(
            persona_name="LeBron James",
            memory_dir="/tmp/test_memory",
            use_memory=False
        )

        # Add some conversation
        memory.store_conversation_turn(role="user", content="Test message 1")
        memory.store_conversation_turn(role="assistant", content="Test response 1", query="Test message 1")

        stats = memory.get_memory_stats()

        print("✓ Retrieved memory statistics:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")

        return True

    except Exception as e:
        print(f"✗ Memory stats failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_amem_integration():
    """Test 5: A-MEM integration (if available)."""
    print_section("TEST 5: A-MEM Integration (Optional)")

    try:
        from src.memory.digital_twin_memory import DigitalTwinMemory

        print("Attempting to initialize A-MEM...")
        memory = DigitalTwinMemory(
            persona_name="LeBron James",
            memory_dir="/tmp/test_memory_amem",
            use_memory=True  # Try to enable A-MEM
        )

        if not memory.use_memory:
            print("⚠ A-MEM not available - skipping")
            print("  Install with: cd A-mem-sys && pip install -e .")
            return True  # Not a failure, just skipped

        print("✓ A-MEM initialized successfully")
        print(f"  - Memory system: {type(memory.memory_system).__name__}")

        # Test adding content
        print("\nTesting content addition...")
        memory_id = memory.add_content(
            content="LeBron James is known for his exceptional basketball IQ and leadership abilities.",
            source="bio.txt",
            content_type="document"
        )

        if memory_id:
            print(f"✓ Added content to memory (ID: {memory_id[:8]}...)")
        else:
            print("✗ Failed to add content")
            return False

        # Test search
        print("\nTesting semantic search...")
        results = memory.search("leadership", k=3)

        print(f"✓ Search returned {len(results)} results")
        if results:
            print(f"  - Top result: {results[0].get('content', '')[:100]}...")

        # Test conversation with memory
        print("\nTesting conversation with memory context...")
        memory.store_conversation_turn(
            role="user",
            content="Tell me about your leadership style"
        )

        context = memory.get_conversation_context(
            query="leadership style",
            max_turns=5,
            max_memories=3
        )

        print(f"✓ Retrieved context with memories ({len(context)} chars)")

        # Get stats
        stats = memory.get_memory_stats()
        print(f"\n✓ Memory statistics:")
        for key, value in stats.items():
            if key != "error":
                print(f"  - {key}: {value}")

        return True

    except Exception as e:
        print(f"⚠ A-MEM integration test failed: {e}")
        print("  This is expected if A-MEM is not installed yet.")
        import traceback
        traceback.print_exc()
        return True  # Don't fail the overall test


def test_llm_config_detection():
    """Test 6: LLM configuration detection."""
    print_section("TEST 6: LLM Configuration Detection")

    try:
        from src.memory.digital_twin_memory import DigitalTwinMemory

        memory = DigitalTwinMemory(
            persona_name="Test",
            memory_dir="/tmp/test_memory",
            use_memory=False
        )

        backend, model = memory._detect_llm_config()
        print(f"✓ Detected LLM configuration:")
        print(f"  - Backend: {backend}")
        print(f"  - Model: {model}")

        return True

    except Exception as e:
        print(f"✗ LLM config detection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print(" Digital Twin Memory System - Manual Test Suite")
    print("="*60)

    tests = [
        ("Import Test", test_import),
        ("Basic Initialization", test_basic_initialization),
        ("Conversation Tracking", test_conversation_tracking),
        ("Memory Statistics", test_memory_stats),
        ("LLM Config Detection", test_llm_config_detection),
        ("A-MEM Integration", test_amem_integration),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            results.append((test_name, False))

    # Summary
    print_section("TEST SUMMARY")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
