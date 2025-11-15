## Code Structure and Best Practices

This document outlines the refactored code structure for the English Teaching Assistant, following professional software engineering standards.

## Architecture Overview

```
src/
├── teacher/                    # English teaching assistant module
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── prompt_loader.py       # Prompt template loader
│   ├── english_teacher_refactored.py  # Main teacher implementation
│   └── prompts/               # Prompt templates
│       ├── system_prompt.txt  # System prompt for teacher
│       ├── greetings.txt      # Greeting messages
│       └── summary_prompt.txt # Conversation summary template
├── voice/                      # Voice interaction components
│   ├── __init__.py
│   ├── audio_recorder.py      # Audio recording
│   ├── speech_to_text.py      # Speech-to-text (Whisper)
│   └── text_to_speech.py      # Text-to-speech (OpenAI TTS)
└── persona/                    # LLM integration
    ├── llm_client.py          # Unified LLM client
    └── ...

tests/
├── conftest.py                # Shared fixtures
├── unit/                      # Unit tests
│   ├── test_prompt_loader.py
│   ├── test_config.py
│   └── test_english_teacher.py
├── integration/               # Integration tests
│   └── test_voice_chat.py
└── fixtures/                  # Test fixtures and mock data
```

## Design Principles

### 1. Separation of Concerns

Each module has a single, well-defined responsibility:

- **config.py**: Configuration management only
- **prompt_loader.py**: Template loading and formatting
- **english_teacher_refactored.py**: Core teaching logic
- **voice/**: Audio I/O operations

### 2. Configuration Management

Configuration is externalized and can be set via:

1. Environment variables
2. Direct instantiation
3. Overrides in code

```python
# From environment
config = TeacherConfig.from_env()

# With overrides
config = TeacherConfig.from_env(
    model="gpt-4",
    temperature=0.8
)

# Direct instantiation
config = TeacherConfig(
    model="gpt-4",
    use_memory=False
)
```

### 3. Prompt Templates

Prompts are separated from code for:
- Easy modification without code changes
- Version control of prompts
- A/B testing of different prompts
- Internationalization support

```python
loader = PromptLoader()

# Load and use templates
system_prompt = loader.get_system_prompt()
greeting = loader.load_greetings()[0]

# Format with variables
summary = loader.format_prompt(
    "summary_prompt",
    conversation_text="..."
)
```

### 4. Error Handling and Logging

Comprehensive error handling with logging:

```python
import logging

logger = logging.getLogger(__name__)

try:
    response = teacher.chat(user_message)
except ValueError as e:
    logger.error(f"Invalid input: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
```

### 5. Dependency Injection

Dependencies are injected for better testability:

```python
# Production
teacher = EnglishTeacher()  # Uses defaults

# Testing
teacher = EnglishTeacher(
    llm_client=mock_client,
    config=test_config,
    prompt_loader=test_loader
)
```

## Testing Strategy

### Unit Tests

Test individual components in isolation:

```bash
# Run all unit tests
pytest tests/unit/

# Run specific test file
pytest tests/unit/test_prompt_loader.py

# Run specific test
pytest tests/unit/test_config.py::TestTeacherConfig::test_default_values
```

### Integration Tests

Test component interactions:

```bash
# Run integration tests
pytest tests/integration/

# Run with coverage
pytest tests/integration/ --cov=src
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html
```

## Configuration Options

### Teacher Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `TEACHER_MODEL` | `gpt-4o` | LLM model to use |
| `TEACHER_TEMPERATURE` | `0.7` | Response randomness (0-1) |
| `TEACHER_MAX_TOKENS` | `300` | Maximum response length |
| `TEACHER_USE_MEMORY` | `true` | Enable conversation memory |
| `TEACHER_MEMORY_DIR` | `data/teacher_memory` | Memory storage path |

### Voice Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `STT_MODEL` | `whisper-1` | Whisper model for STT |
| `STT_LANGUAGE` | `en` | Speech recognition language |
| `TTS_MODEL` | `tts-1` | TTS model (`tts-1` or `tts-1-hd`) |
| `TTS_VOICE` | `nova` | Voice to use |
| `AUDIO_SAMPLE_RATE` | `16000` | Audio sample rate (Hz) |
| `AUDIO_CHANNELS` | `1` | Audio channels (1=mono, 2=stereo) |

## Usage Examples

### Basic Usage

```python
from src.teacher.english_teacher_refactored import EnglishTeacher

# Initialize teacher
teacher = EnglishTeacher()

# Chat
response = teacher.chat("Hello, I want to practice English")
print(response)

# Get stats
stats = teacher.get_stats()
print(f"Exchanges: {stats['total_exchanges']}")

# Save session
filepath = teacher.save_session()
```

### Custom Configuration

```python
from src.teacher.english_teacher_refactored import EnglishTeacher
from src.teacher.config import TeacherConfig

# Custom config
config = TeacherConfig(
    model="gpt-3.5-turbo",
    temperature=0.9,
    use_memory=False,
    max_tokens=200
)

teacher = EnglishTeacher(config=config)
```

### Testing

```python
from src.teacher.english_teacher_refactored import EnglishTeacher
from unittest.mock import Mock

# Mock LLM client
mock_client = Mock()
mock_client.generate.return_value = "Mock response"

# Create teacher with mock
teacher = EnglishTeacher(llm_client=mock_client)
response = teacher.chat("Test")

assert mock_client.generate.called
```

## Best Practices

### 1. Always Use Configuration Objects

❌ Don't:
```python
teacher = EnglishTeacher()
teacher.temperature = 0.9  # Modifying after creation
```

✅ Do:
```python
config = TeacherConfig(temperature=0.9)
teacher = EnglishTeacher(config=config)
```

### 2. Use Logging, Not Print

❌ Don't:
```python
print("Processing message...")
```

✅ Do:
```python
logger.info("Processing message...")
```

### 3. Handle Errors Explicitly

❌ Don't:
```python
response = teacher.chat(user_input)  # What if it fails?
```

✅ Do:
```python
try:
    response = teacher.chat(user_input)
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    return error_response
except Exception as e:
    logger.error(f"Failed to generate response: {e}")
    return fallback_response
```

### 4. Write Tests

For every new feature:
1. Write unit tests for individual functions
2. Write integration tests for workflows
3. Ensure >80% code coverage

### 5. Document Public APIs

```python
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
```

## Performance Optimization

### Prompt Caching

Prompts are automatically cached after first load:

```python
loader = PromptLoader()

# First call: loads from disk
prompt1 = loader.load_prompt("system_prompt")

# Second call: returns cached version
prompt2 = loader.load_prompt("system_prompt")  # Fast!
```

### Context Window Management

Conversation history is automatically limited:

```python
config = TeacherConfig(
    max_history_exchanges=10  # Only keep last 10 exchanges
)
```

This prevents:
- Token limit exceeded errors
- Slow API responses
- High costs

## Migration Guide

### From Old to New Implementation

1. **Update imports**:
```python
# Old
from src.teacher.english_teacher import EnglishTeacher

# New
from src.teacher.english_teacher_refactored import EnglishTeacher
```

2. **Use configuration**:
```python
# Old
teacher = EnglishTeacher(use_memory=False, memory_dir="path")

# New
config = TeacherConfig(use_memory=False, memory_dir="path")
teacher = EnglishTeacher(config=config)
```

3. **Update tests**:
```python
# Old: Mocking was difficult

# New: Easy mocking with dependency injection
mock_client = Mock()
teacher = EnglishTeacher(llm_client=mock_client)
```

## Troubleshooting

### Import Errors

If you get import errors, ensure you're running from project root:

```bash
cd OpenDigitalTwin
python -m pytest tests/
```

### Configuration Not Loading

Check that `.env` file is in `config/` directory:

```bash
ls -la config/.env
```

### Tests Failing

Run with verbose output:

```bash
pytest -vv tests/unit/test_prompt_loader.py
```

Check test coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

## Contributing

When adding new features:

1. Update configuration in `config.py`
2. Add prompts to `prompts/` directory
3. Write unit tests
4. Write integration tests
5. Update this documentation
6. Run full test suite: `pytest`

## Further Reading

- [Testing Guide](TEST_PLAN.md)
- [English Teacher Setup](ENGLISH_TEACHER_SETUP.md)
- [Memory System](MEMORY_SYSTEM.md)
