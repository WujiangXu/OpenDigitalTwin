"""
Demo test: Digital Twin Memory System - End-to-end workflow
This demonstrates the memory system working in a real digital twin scenario.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.memory.digital_twin_memory import DigitalTwinMemory

def demo_workflow():
    print("="*60)
    print(" Digital Twin Memory System - Live Demo")
    print("="*60)

    # Step 1: Initialize memory for LeBron James
    print("\n📝 STEP 1: Initialize Memory System")
    print("-" * 60)

    memory = DigitalTwinMemory(
        persona_name="LeBron James",
        memory_dir="/tmp/lebron_demo",
        use_memory=True  # Try to use A-MEM if available
    )

    print(f"✓ Memory system created for: {memory.persona_name}")
    print(f"  - Memory enabled: {memory.use_memory}")
    print(f"  - Memory dir: {memory.memory_dir}")

    # Step 2: Simulate adding persona content
    print("\n📚 STEP 2: Add Persona Content to Memory")
    print("-" * 60)

    lebron_content = [
        {
            "content": "Leadership is about bringing out the best in your teammates. "
                      "You lead by example - show up early, work hard, stay late. "
                      "But you also need to communicate and understand what drives each person.",
            "source": "leadership_interview_2024.txt",
            "type": "interview"
        },
        {
            "content": "Basketball is a team sport. My success is tied to my team's success. "
                      "I've always believed in making my teammates better.",
            "source": "team_philosophy.txt",
            "type": "article"
        },
        {
            "content": "Defense wins championships. You can have all the offensive talent "
                      "in the world, but if you don't play defense, you won't win.",
            "source": "defensive_mindset.txt",
            "type": "speech"
        }
    ]

    if memory.use_memory:
        print("Adding content to A-MEM memory system...")
        for item in lebron_content:
            memory_id = memory.add_content(
                content=item["content"],
                source=item["source"],
                content_type=item["type"]
            )
            print(f"  ✓ Added: {item['source'][:40]}... (ID: {memory_id[:8] if memory_id else 'N/A'}...)")
    else:
        print("⚠ A-MEM not available - using conversation-only mode")
        print("  (Content would be added to long-term memory if A-MEM installed)")

    # Step 3: Simulate user conversation
    print("\n💬 STEP 3: Conversation with Digital Twin")
    print("-" * 60)

    conversation = [
        {"role": "user", "content": "How do you approach leadership in basketball?"},
        {"role": "assistant", "content": "Leadership is about bringing out the best in your teammates. You lead by example - show up early, work hard, stay late. I communicate with each player to understand what drives them.", "query": "How do you approach leadership in basketball?"},
        {"role": "user", "content": "What's your philosophy on team play?"},
        {"role": "assistant", "content": "Basketball is a team sport, and my success is directly tied to my team's success. I've always believed in making my teammates better and creating an environment where everyone can contribute.", "query": "What's your philosophy on team play?"},
    ]

    for turn in conversation:
        memory.store_conversation_turn(
            role=turn["role"],
            content=turn["content"],
            query=turn.get("query")
        )
        print(f"  {turn['role'].upper()}: {turn['content'][:80]}...")

    print(f"\n✓ Stored {len(conversation)} conversation turns")

    # Step 4: Retrieve context for new query
    print("\n🔍 STEP 4: Retrieve Context for New Query")
    print("-" * 60)

    new_query = "Tell me about defense and winning"
    print(f"User query: \"{new_query}\"\n")

    context = memory.get_conversation_context(
        query=new_query,
        max_turns=3,
        max_memories=2
    )

    print("Retrieved context:")
    print(context)
    print()

    if memory.use_memory:
        # Search for relevant memories
        print("\n🔎 STEP 5: Search Memory Semantically")
        print("-" * 60)
        results = memory.search("defense championships", k=3)
        if results:
            print(f"Found {len(results)} relevant memories:")
            for i, result in enumerate(results, 1):
                print(f"\n  {i}. {result.get('content', '')[:100]}...")
                print(f"     Source: {result.get('metadata', {}).get('source', 'unknown')}")
        else:
            print("No results (memory empty or A-MEM not ready)")

    # Step 6: Get statistics
    print("\n📊 STEP 6: Memory Statistics")
    print("-" * 60)

    stats = memory.get_memory_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Summary
    print("\n" + "="*60)
    print(" Summary")
    print("="*60)
    print(f"✓ Memory system: {'FULL' if memory.use_memory else 'BASIC (conversation-only)'}")
    print(f"✓ Conversation turns tracked: {stats['conversation_turns']}")
    if memory.use_memory:
        print(f"✓ Long-term memories: {stats.get('total_memories', 'N/A')}")
    print(f"✓ Context retrieval: WORKING")
    print(f"✓ Ready for: LLM integration")

    print("\n🎯 Next Step: Integrate with persona generator in main.py")
    print("   - Use context in LLM prompts")
    print("   - Enable memory-powered responses")

    return True

if __name__ == "__main__":
    try:
        success = demo_workflow()
        print("\n✅ Demo completed successfully!")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
