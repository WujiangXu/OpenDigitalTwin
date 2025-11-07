# Digital Twin Memory System

## Overview

The Digital Twin Memory System provides advanced memory capabilities for digital twin personas, enabling them to:

- **Remember conversations** across multiple sessions
- **Search semantically** for relevant content (not just keyword matching)
- **Learn from interactions** and evolve over time
- **Retrieve context** intelligently for more accurate responses

The system is built on [A-MEM](https://github.com/WujiangXu/A-mem-sys) (Agentic Memory for LLM Agents) from NeurIPS 2025, which provides state-of-the-art memory management for AI agents.

## Features

### 🎯 Core Capabilities

1. **Semantic Search**
   - Hybrid retrieval combining semantic similarity (embeddings) and keyword matching (BM25)
   - Understands meaning, not just exact word matches
   - Example: Search for "employment trends" finds content about "labor market" and "job growth"

2. **Conversation Memory**
   - Tracks multi-turn dialogues
   - Maintains conversation context
   - Stores important turns in long-term memory

3. **Memory Evolution**
   - Automatically consolidates related memories
   - Creates semantic links between content
   - Learns from user interactions

4. **LLM-Powered Metadata**
   - Auto-generates keywords, context, and tags
   - Enriches search with metadata
   - Uses the same LLM backend as your digital twin

### 🔧 Architecture

```
┌────────────────────────────────────────────────┐
│         DigitalTwinMemory (our wrapper)        │
├────────────────────────────────────────────────┤
│  • Persona-specific memory management          │
│  • Conversation tracking                       │
│  • Context retrieval for LLM                   │
│  • Statistics and monitoring                   │
└─────────────────┬──────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────────────┐
│       A-MEM (AgenticMemorySystem)              │
├────────────────────────────────────────────────┤
│  • Vector storage (ChromaDB)                   │
│  • Semantic + BM25 hybrid search               │
│  • Memory linking and evolution                │
│  • LLM-based metadata generation               │
└────────────────────────────────────────────────┘
```

## Installation

### Step 1: Install A-MEM

```bash
# Clone the A-MEM repository
git clone https://github.com/WujiangXu/A-mem-sys.git

# Install in editable mode
cd A-mem-sys
pip install -e .
```

This will install all dependencies including:
- `chromadb` (vector database)
- `sentence-transformers` (embeddings)
- `litellm` (unified LLM interface)
- `torch` (required for embeddings, ~900MB)

### Step 2: Verify Installation

```bash
# Run the manual test suite
python tests/manual_test_memory.py
```

Expected output:
```
🎉 All tests passed!
```

### Step 3: Configure API Keys

Set your LLM API key (OpenAI or Anthropic):

```bash
# For OpenAI
export OPENAI_API_KEY="sk-..."

# OR for Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

Or add to `config/config.json`:
```json
{
  "openai_api_key": "sk-...",
  "default_model": "gpt-4o-mini"
}
```

## Usage

### Basic Usage

```python
from src.memory.digital_twin_memory import DigitalTwinMemory

# Initialize memory for a persona
memory = DigitalTwinMemory(
    persona_name="LeBron James",
    use_memory=True  # Enable A-MEM features
)

# Add content to memory
memory.add_content(
    content="Leadership means bringing out the best in your teammates",
    source="leadership_guide.txt",
    content_type="document"
)

# Search for relevant content
results = memory.search("team leadership", k=5)
for result in results:
    print(result['content'])

# Track conversations
memory.store_conversation_turn(
    role="user",
    content="How do you approach leadership?"
)

# Get context for LLM response
context = memory.get_conversation_context(
    query="leadership approach",
    max_turns=5,      # Include last 5 conversation turns
    max_memories=3    # Include top 3 relevant memories
)
```

### Advanced Usage

#### Custom LLM Backend

```python
memory = DigitalTwinMemory(
    persona_name="LeBron James",
    llm_backend="claude",  # or "openai"
    llm_model="claude-3-sonnet-20240229",
    use_memory=True
)
```

#### Custom Memory Directory

```python
memory = DigitalTwinMemory(
    persona_name="LeBron James",
    memory_dir="./my_custom_data/memories",
    use_memory=True
)
```

#### Bulk Content Addition

```python
# Add multiple documents
documents = [
    {"content": "Doc 1 content", "source": "doc1.txt"},
    {"content": "Doc 2 content", "source": "doc2.txt"},
    {"content": "Doc 3 content", "source": "doc3.txt"},
]

for doc in documents:
    memory.add_content(
        content=doc["content"],
        source=doc["source"],
        content_type="document"
    )
```

#### Memory Statistics

```python
stats = memory.get_memory_stats()
print(f"Total memories: {stats.get('total_memories', 0)}")
print(f"Conversation turns: {stats['conversation_turns']}")
print(f"Evolution count: {stats.get('evolution_count', 0)}")
```

## Integration with Digital Twin

### Building a Persona with Memory

```python
from src.persona.generator import PersonaGenerator
from src.memory.digital_twin_memory import DigitalTwinMemory

# 1. Build persona profile
generator = PersonaGenerator()
profile = generator.generate_persona(
    name="LeBron James",
    content_sources=["press_conference_1.txt", "interview_1.txt"]
)

# 2. Initialize memory system
memory = DigitalTwinMemory(
    persona_name="LeBron James",
    use_memory=True
)

# 3. Load persona content into memory
for source in profile['sources']:
    memory.add_content(
        content=source['content'],
        source=source['url'],
        content_type=source['type']
    )

# 4. Use memory-powered responses
def respond_as_persona(query: str) -> str:
    # Get conversation context from memory
    context = memory.get_conversation_context(query)

    # Generate response using persona + context
    response = generator.generate_response(
        persona=profile,
        query=query,
        context=context
    )

    # Store the conversation
    memory.store_conversation_turn(role="user", content=query)
    memory.store_conversation_turn(
        role="assistant",
        content=response,
        query=query
    )

    return response

# Use it
response = respond_as_persona("How do you approach leadership in basketball?")
print(response)
```

## Configuration

### Memory System Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `persona_name` | (required) | Name of the digital twin persona |
| `memory_dir` | `./data/{persona}/memory` | Directory for memory storage |
| `llm_backend` | Auto-detect | LLM provider ("openai" or "claude") |
| `llm_model` | Backend-specific | Model name (e.g., "gpt-4o-mini") |
| `use_memory` | `True` | Enable/disable A-MEM features |

### A-MEM Parameters

The A-MEM system has additional configuration options:

- `evolution_threshold`: Number of memories before consolidation (default: 100)
- `chromadb_path`: Custom path for ChromaDB storage
- Various retrieval and ranking parameters

See [A-MEM documentation](https://github.com/WujiangXu/A-mem-sys) for details.

## Testing

### Manual Testing

Run the manual test suite:

```bash
python tests/manual_test_memory.py
```

This will test:
1. Module imports
2. Basic initialization
3. Conversation tracking
4. Memory statistics
5. LLM configuration
6. A-MEM integration (if installed)

### Pytest Testing

Run comprehensive tests with pytest:

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/test_digital_twin_memory.py -v

# Run specific test class
pytest tests/test_digital_twin_memory.py::TestConversationTracking -v

# Run with coverage
pytest tests/test_digital_twin_memory.py --cov=src/memory
```

### Test Categories

1. **Initialization Tests**: Verify memory system initialization
2. **Content Addition Tests**: Test adding content to memory
3. **Semantic Search Tests**: Verify search functionality
4. **Conversation Tracking Tests**: Test multi-turn conversations
5. **Memory Statistics Tests**: Verify monitoring capabilities
6. **Error Handling Tests**: Test edge cases and failures
7. **Integration Tests**: End-to-end workflow validation
8. **Performance Tests**: Verify scalability

## Troubleshooting

### A-MEM Not Installed

**Symptom:**
```
⚠ A-MEM not installed. Memory features disabled.
```

**Solution:**
```bash
cd A-mem-sys
pip install -e .
```

### Missing API Key

**Symptom:**
```
Error: No API key found for OpenAI
```

**Solution:**
```bash
export OPENAI_API_KEY="sk-..."
# or
export ANTHROPIC_API_KEY="sk-ant-..."
```

### PyTorch Download Slow

**Symptom:** Installation hangs downloading PyTorch (899 MB)

**Solution:** Be patient - this is a large file. Or use a pre-installed PyTorch:
```bash
# Install PyTorch separately with CPU-only version (smaller)
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Memory Directory Permissions

**Symptom:**
```
PermissionError: Cannot create directory
```

**Solution:**
```python
# Use a custom directory with write permissions
memory = DigitalTwinMemory(
    persona_name="...",
    memory_dir="/tmp/my_memory"
)
```

## Performance

### Benchmarks

Based on testing with 50-100 documents:

| Operation | Latency | Notes |
|-----------|---------|-------|
| Add Content | 1-3s | Depends on LLM API latency for metadata generation |
| Search | <100ms | Fast ChromaDB vector search |
| Get Context | <200ms | Includes search + formatting |
| Store Turn | <50ms | In-memory operation |

### Optimization Tips

1. **Batch content addition**: Add multiple documents in succession
2. **Adjust evolution threshold**: Higher = fewer consolidations, faster
3. **Limit search results**: Use `k=3` instead of `k=10` for faster context retrieval
4. **Use local embeddings**: Sentence-transformers are faster than API-based embeddings

## Limitations

1. **Requires LLM API**: Metadata generation needs OpenAI or Anthropic API
2. **Memory size**: ChromaDB scales well, but very large datasets (>100k memories) may slow down
3. **No multi-user**: Current implementation is single-user per persona
4. **Evolution not real-time**: Memory consolidation happens after threshold, not continuously

## Roadmap

Planned enhancements:

- [ ] User modeling: Personalized responses per user
- [ ] Memory analytics: Visualize memory relationships
- [ ] Export/import: Save and load memory systems
- [ ] Multi-modal: Support audio and visual content
- [ ] Distributed: Share memories across instances

## References

- **A-MEM Paper**: WujiangXu et al., "A-MEM: Agentic Memory for LLM Agents", NeurIPS 2025
- **A-MEM Repository**: https://github.com/WujiangXu/A-mem-sys
- **ChromaDB**: https://www.trychroma.com/
- **Sentence Transformers**: https://www.sbert.net/

## License

This memory system integration is part of OpenDigitalTwin. See main project license.

A-MEM is used under its original license (see A-mem-sys repository).
