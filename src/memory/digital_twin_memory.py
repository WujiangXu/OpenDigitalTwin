"""
Digital Twin Memory System using A-MEM.

This module provides a memory layer for digital twins that enables:
- Semantic search for content retrieval
- Conversation history tracking
- Memory evolution and consolidation
- LLM-powered metadata generation
"""

import os
import json
from typing import List, Dict, Optional, Any
from datetime import datetime


class DigitalTwinMemory:
    """
    Memory manager for digital twins using A-MEM system.

    This class wraps the AgenticMemorySystem from A-MEM and provides
    a simplified API tailored for digital twin use cases.

    Features:
    - Semantic + BM25 hybrid search
    - Automatic metadata generation (keywords, context, tags)
    - Conversation history tracking
    - Memory evolution and consolidation
    """

    def __init__(
        self,
        persona_name: str,
        memory_dir: str = None,
        llm_backend: str = None,
        llm_model: str = None,
        use_memory: bool = True
    ):
        """
        Initialize digital twin memory system.

        Args:
            persona_name: Name of the digital twin persona (e.g., "LeBron James")
            memory_dir: Directory to store memory data (default: ./data/{persona_name}/memory)
            llm_backend: LLM backend ("openai" or "claude", None = auto-detect from config)
            llm_model: Model name (default: gpt-4o-mini for OpenAI, claude-3-sonnet for Claude)
            use_memory: Whether to enable memory features (can disable for testing)
        """
        self.persona_name = persona_name
        self.use_memory = use_memory

        # Set up memory directory
        if memory_dir is None:
            memory_dir = os.path.join("data", persona_name.replace(" ", "_").lower(), "memory")
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)

        # Initialize A-MEM system
        self.memory_system = None
        if use_memory:
            try:
                from agentic_memory import AgenticMemorySystem

                # Determine LLM backend from config if not specified
                if llm_backend is None:
                    llm_backend, llm_model = self._detect_llm_config()

                # Initialize A-MEM with appropriate LLM backend
                self.memory_system = AgenticMemorySystem(
                    llm_backend=llm_backend,
                    llm_model=llm_model,
                    chromadb_path=os.path.join(self.memory_dir, "chromadb"),
                    evolution_threshold=100  # Consolidate memories after 100 additions
                )
                print(f"✓ Memory system initialized for '{persona_name}' using {llm_backend}/{llm_model}")

            except ImportError:
                print("⚠ A-MEM not installed. Memory features disabled.")
                print("  Install with: pip install -e A-mem-sys")
                self.use_memory = False
            except Exception as e:
                print(f"⚠ Failed to initialize memory system: {e}")
                print("  Memory features disabled.")
                self.use_memory = False

        # Conversation history (in-memory, also backed by A-MEM)
        self.conversation_history: List[Dict[str, Any]] = []

    def _detect_llm_config(self) -> tuple[str, str]:
        """
        Detect LLM configuration from config files or environment.

        Returns:
            (backend, model) tuple
        """
        # Check for API keys to determine available backend
        if os.getenv("OPENAI_API_KEY"):
            return "openai", "gpt-4o-mini"
        elif os.getenv("ANTHROPIC_API_KEY"):
            return "claude", "claude-3-sonnet-20240229"

        # Try reading from config file
        config_path = "config/config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    if config.get("openai_api_key"):
                        return "openai", "gpt-4o-mini"
                    elif config.get("anthropic_api_key"):
                        return "claude", "claude-3-sonnet-20240229"
            except Exception as e:
                print(f"⚠ Error reading config: {e}")

        # Default to OpenAI
        return "openai", "gpt-4o-mini"

    def add_content(
        self,
        content: str,
        source: str = None,
        content_type: str = "document",
        metadata: Dict[str, Any] = None
    ) -> Optional[str]:
        """
        Add content to memory system.

        Args:
            content: Text content to store
            source: Source of content (e.g., URL, file path)
            content_type: Type of content ("document", "conversation", "speech", etc.)
            metadata: Optional metadata (will be auto-generated if not provided)

        Returns:
            Memory ID if successful, None otherwise
        """
        if not self.use_memory or not self.memory_system:
            return None

        try:
            # Prepare metadata
            if metadata is None:
                metadata = {}

            metadata.update({
                "source": source or "unknown",
                "content_type": content_type,
                "persona": self.persona_name,
                "timestamp": datetime.now().isoformat()
            })

            # Add to A-MEM (will auto-generate keywords, context, tags)
            memory_id = self.memory_system.add_note(
                content=content,
                metadata=metadata
            )

            return memory_id

        except Exception as e:
            print(f"⚠ Error adding content to memory: {e}")
            return None

    def search(
        self,
        query: str,
        k: int = 5,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search memory using semantic similarity.

        Args:
            query: Search query
            k: Number of results to return
            filters: Optional metadata filters

        Returns:
            List of memory items with relevance scores
        """
        if not self.use_memory or not self.memory_system:
            return []

        try:
            # Use A-MEM's agentic search (returns results + linked memories)
            results = self.memory_system.search_agentic(
                query=query,
                k=k,
                filters=filters
            )

            return results

        except Exception as e:
            print(f"⚠ Error searching memory: {e}")
            return []

    def get_conversation_context(
        self,
        query: str,
        max_turns: int = 5,
        max_memories: int = 3
    ) -> str:
        """
        Retrieve conversation context for a query.

        Combines:
        1. Recent conversation history
        2. Relevant memories from past interactions

        Args:
            query: Current user query
            max_turns: Maximum conversation turns to include
            max_memories: Maximum related memories to retrieve

        Returns:
            Formatted context string for LLM
        """
        context_parts = []

        # Add recent conversation history
        if self.conversation_history:
            recent_turns = self.conversation_history[-max_turns:]
            context_parts.append("## Recent Conversation")
            for turn in recent_turns:
                role = turn.get("role", "unknown")
                content = turn.get("content", "")
                context_parts.append(f"**{role.capitalize()}**: {content}")

        # Search for relevant memories
        if self.use_memory and max_memories > 0:
            memories = self.search(query, k=max_memories)
            if memories:
                context_parts.append("\n## Relevant Context from Memory")
                for i, mem in enumerate(memories, 1):
                    content = mem.get("content", "")
                    source = mem.get("metadata", {}).get("source", "unknown")
                    context_parts.append(f"{i}. {content}\n   (Source: {source})")

        return "\n\n".join(context_parts)

    def store_conversation_turn(
        self,
        role: str,
        content: str,
        query: str = None
    ):
        """
        Store a conversation turn in memory.

        Args:
            role: "user" or "assistant"
            content: Message content
            query: Original user query (for assistant responses)
        """
        # Add to in-memory conversation history
        turn = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        if query:
            turn["query"] = query

        self.conversation_history.append(turn)

        # Also store important turns in long-term memory
        if self.use_memory and role == "assistant":
            # Store assistant responses as memories
            self.add_content(
                content=f"Q: {query}\nA: {content}",
                content_type="conversation",
                metadata={
                    "conversation_turn": len(self.conversation_history),
                    "query": query
                }
            )

    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory system statistics.

        Returns:
            Dictionary with memory stats
        """
        stats = {
            "persona": self.persona_name,
            "memory_enabled": self.use_memory,
            "conversation_turns": len(self.conversation_history),
            "memory_dir": self.memory_dir
        }

        if self.use_memory and self.memory_system:
            try:
                # Get total memories from A-MEM
                stats["total_memories"] = len(self.memory_system.memories)
                stats["evolution_count"] = self.memory_system.evolution_counter
            except Exception as e:
                stats["error"] = str(e)

        return stats

    def clear_conversation_history(self):
        """Clear in-memory conversation history (does not affect long-term memories)."""
        self.conversation_history = []

    def reset_memory(self, confirm: bool = False):
        """
        Reset entire memory system (DESTRUCTIVE).

        Args:
            confirm: Must be True to actually reset
        """
        if not confirm:
            print("⚠ Reset not confirmed. Set confirm=True to reset memory.")
            return

        # Clear conversation history
        self.conversation_history = []

        # Reset A-MEM if enabled
        if self.use_memory and self.memory_system:
            try:
                # Delete ChromaDB data
                import shutil
                chromadb_path = os.path.join(self.memory_dir, "chromadb")
                if os.path.exists(chromadb_path):
                    shutil.rmtree(chromadb_path)

                # Reinitialize
                from agentic_memory import AgenticMemorySystem
                llm_backend, llm_model = self._detect_llm_config()
                self.memory_system = AgenticMemorySystem(
                    llm_backend=llm_backend,
                    llm_model=llm_model,
                    chromadb_path=chromadb_path,
                    evolution_threshold=100
                )

                print(f"✓ Memory reset for '{self.persona_name}'")

            except Exception as e:
                print(f"⚠ Error resetting memory: {e}")


# Convenience function for backward compatibility
class MemoryManager(DigitalTwinMemory):
    """Alias for DigitalTwinMemory for backward compatibility."""
    pass
