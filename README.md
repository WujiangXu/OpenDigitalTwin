# OpenDigitalTwin

An open-source **multi-modal agentic digital twin system** that creates AI replicas capable of learning, remembering, and adapting through interactions.

## What is OpenDigitalTwin?

OpenDigitalTwin creates **dynamic AI replicas** of individuals by:
1. **Learning** from their writings, speeches, and communications
2. **Remembering** past conversations and interactions (future)
3. **Adapting** personas based on feedback and new information (future)
4. **Personalizing** responses for different users (future)

Unlike static chatbots, OpenDigitalTwin builds digital twins that can evolve and improve over time.

## Current Features (v1.0)

### ✅ Static Persona Building
- Extract content from web, documents, and APIs
- Analyze writing style, communication patterns, decision-making approach
- Generate responses mimicking the individual's style

### ✅ Multiple Data Sources
- **Jina AI**: Free web extraction (no API key needed)
- **Firecrawl**: High-quality scraping with intelligent search
- **Document parsing**: PDFs, text files
- **Auto-discovery**: Automatically find and extract content

### ✅ CLI Interface
- Simple command-line tools
- Extract → Analyze → Query/Chat workflow

## Capabilities

### ✅ Agentic Memory System (Phase 1 - NEW!)
Based on [A-MEM](https://github.com/WujiangXu/A-mem-sys) (NeurIPS 2025):
- **✅ Semantic Search**: Hybrid retrieval (semantic + BM25) for intelligent context retrieval
- **✅ Conversation Memory**: Track and recall multi-turn dialogue history
- **✅ Memory Evolution**: Consolidate and evolve memories based on relationships
- **✅ LLM-Powered**: Automatic metadata generation (keywords, context, tags)
- **🔄 User Modeling**: Personalized responses per user (coming soon)
- **🔄 Memory Analytics**: Visualize memory relationships (coming soon)

📚 See [docs/MEMORY_SYSTEM.md](docs/MEMORY_SYSTEM.md) for detailed documentation and usage.

## Future Capabilities (Roadmap)

### 🔄 User Modeling (Phase 3)
- Track user preferences and patterns
- Personalize responses per user
- Learn from query history

### 🔄 Adaptive Learning (Phase 4)
- Continuous persona improvement
- Feedback integration
- Version control for personas

### 📋 Multi-Modal Support (Future)
- **Audio**: Speech analysis, tone/pace understanding
- **Visual**: Chart/presentation extraction
- **Multi-modal fusion**: Coherent cross-modal personas

## Architecture

### Extractor

Collects and processes data from multiple sources to build a comprehensive profile:
- **Jina AI Reader**: Free, simple web content extraction (no API key required)
- **Firecrawl + Tavily**: Best performance with intelligent search and scraping (free tier available)
- Document parsing (text files, PDFs)
- Automatic Powell speech extraction from Federal Reserve website

### Persona Builder

Analyzes extracted data and manages LLM interactions to create an authentic digital twin:
- Profile analysis and pattern extraction using LLMs
- Writing style and communication pattern analysis
- Decision-making style characterization
- Context-aware prompt building
- Response generation via LLM API calls

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp config/.env.example config/.env

# Edit config/.env with your API keys
nano config/.env  # Add your OpenAI or Anthropic API key
```

**Minimum configuration** in `config/.env`:
```bash
LLM_PROVIDER=openai  # or 'anthropic'
OPENAI_API_KEY=your_key_here
EXTRACTOR_TYPE=jina  # or 'firecrawl'
```

---

## Use Case: Digital LeBron James

This example demonstrates building a digital twin of NBA star LeBron James that can communicate in his style based on interviews, social media posts, and public statements.

### Step 1: Extract LeBron's Content

```bash
# Extract from interviews, articles, and social media
python main.py extract --url https://example.com/lebron-interview-1
python main.py extract --url https://example.com/lebron-interview-2
# ... add more URLs

# Or extract from local files
python main.py extract --file lebron_interviews.pdf --file social_media_posts.txt

# Output:
# ✓ Extracted content
# ✓ Saved 15 items
```

### Step 2: Build LeBron's Persona

```bash
# Analyze all extracted content to build persona profile
python main.py analyze --name "LeBron James"

# The system will analyze:
# - Writing style (motivational, confident, authentic)
# - Communication patterns (inspirational, team-focused)
# - Key topics (basketball, leadership, community, family)
# - Decision-making approach (strategic with emotional intelligence)
```

### Step 3: Query the Digital Twin

```bash
# Ask a question
python main.py query "What's your approach to leadership?"
```

**Example Output**:
```
LeBron James:
Leadership is about more than just being the best player on the
court. It's about elevating everyone around you, making your
teammates better. I've always believed that my success is tied
to my team's success. You lead by example - show up early, work
hard, stay late. But you also need to communicate, understand
what drives each person, and create an environment where everyone
feels valued and empowered to contribute...
```

### Step 4: Interactive Chat

```bash
# Chat with Digital LeBron
python main.py chat --name "LeBron James"

You: How do you stay motivated after all these years?
LeBron: You know, for me it's never been just about basketball...

You: What advice would you give to young players?
LeBron: First, fall in love with the process, not just the outcome...

You: exit
```

### Verify System Status

```bash
python main.py status

# Output:
# Content items in database: 15
# Persona profile: LeBron James ✓
# Configuration:
#   Extractor: jina
#   LLM Provider: openai
```

---

## Building Your Own Digital Twin

The same workflow applies to any individual:

```bash
# 1. Extract content from custom sources
python main.py extract --url https://yourblog.com/articles

# 2. Or extract from local files
python main.py extract --file writings.pdf --file speeches.txt

# 3. Build persona
python main.py analyze --name "Your Name"

# 4. Query the digital twin
python main.py query "What is your view on AI?"

# 5. Interactive chat
python main.py chat --name "Your Name"
```

## CLI Commands Reference

### Data Extraction
```bash
python main.py extract --url <url>           # Extract from URL
python main.py extract --file <path>         # Extract from file
python main.py extract --powell --num 10     # Auto-extract Powell speeches
python main.py info                          # View extractor options
```

### Persona Building
```bash
python main.py analyze --name "Name"         # Build persona from extracted content
python main.py status                        # Check system status
```

### Interaction
```bash
python main.py query "question"              # Ask single question
python main.py chat --name "Name"            # Interactive chat
python main.py fomc --inflation X% --unemployment Y%  # Generate FOMC decision
```

## Extractor Options

| Feature | Jina AI (Default) | Firecrawl |
|---------|-------------------|-----------|
| **Cost** | FREE (no API key) | FREE tier |
| **Setup** | Zero config | API key needed |
| **Best For** | Quick start | Complex sites |

## Project Structure

```
OpenDigitalTwin/
├── src/
│   ├── extractor/          # Data collection modules
│   ├── persona/            # Persona analysis & generation
│   ├── memory/             # Memory system (A-MEM integration)
│   └── cli.py              # CLI interface
├── tests/                  # Test suite
│   ├── test_digital_twin_memory.py    # Pytest tests
│   └── manual_test_memory.py          # Manual test script
├── docs/                   # Documentation
│   ├── MEMORY_SYSTEM.md    # Memory system guide
│   └── TEST_PLAN.md        # Testing documentation
├── A-mem-sys/              # A-MEM submodule
├── config/.env             # Configuration
├── data/database.db        # SQLite storage
├── main.py                 # Entry point
└── requirements.txt        # Dependencies
```

## Documentation

- **README.md** (this file): Quick start and LeBron James use case
- **[docs/MEMORY_SYSTEM.md](docs/MEMORY_SYSTEM.md)**: Memory system documentation
- **[docs/TEST_PLAN.md](docs/TEST_PLAN.md)**: Testing strategy and results

## API Keys

- **OpenAI** or **Anthropic**: Required for LLM (persona analysis & generation)
- **Jina AI**: Optional, free tier (default extractor, no key needed)
- **Firecrawl**: Optional, free tier (advanced extractor)

Get API keys:
- OpenAI: https://platform.openai.com
- Anthropic: https://console.anthropic.com
- Firecrawl: https://firecrawl.dev

## Contributing

Contributions welcome! Areas of interest:
- Memory system implementation (Phase 1)
- Semantic retrieval improvements
- Multi-modal support (audio/visual)
- User modeling and personalization

## License

MIT License


