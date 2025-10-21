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

## Future Capabilities (Roadmap)

### 🔄 Agentic Memory System (Phase 1)
Based on [A-MEM](https://github.com/WujiangXu/A-mem-sys) (NeurIPS 2025):
- **Long-term Memory**: Dynamic persona evolution
- **Working Memory**: Multi-turn conversation context
- **Episodic Memory**: Interaction history tracking
- **Semantic Search**: Meaning-based retrieval
- **External Input**: Manual content addition

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

## Use Case: Digital Jerome Powell for FOMC Decisions

This example demonstrates building a digital twin of Federal Reserve Chair Jerome Powell that can generate FOMC (Federal Open Market Committee) meeting decisions based on economic indicators.

### Step 1: Extract Powell's Speeches

```bash
# Automatically find and extract Powell speeches from federalreserve.gov
python main.py extract --powell --num 10

# Output:
# ✓ Extracted 10 speeches
# ✓ Saved 10 items
```

### Step 2: Build Powell's Persona

```bash
# Analyze all extracted content to build persona profile
python main.py analyze --name "Jerome Powell"

# The system will analyze:
# - Writing style (formal, data-driven, measured tone)
# - Communication patterns (structured, institutional language)
# - Key topics (dual mandate, inflation, labor market)
# - Decision-making approach (data-driven with judgment)
```

### Step 3: Generate FOMC Decision

```bash
# Provide economic indicators to generate FOMC statement
python main.py fomc --inflation 3.5% --unemployment 3.8% --gdp-growth 2.3%
```

**Example Output**:
```
============================================================
FOMC DECISION STATEMENT
============================================================
Policy Decision
- The Committee decided to maintain the target range for the
  federal funds rate at 5-1/4 to 5-1/2 percent...

Rationale
- Recent indicators suggest that economic activity has been
  expanding at a moderate pace. Inflation has eased over the
  past year but remains elevated at 3.5 percent...

Forward Guidance
- The Committee does not expect it will be appropriate to
  reduce the target range until it has gained greater
  confidence that inflation is moving sustainably toward
  2 percent...
```

### Step 4: Interactive Chat (Optional)

```bash
# Chat with Digital Powell
python main.py chat --name "Jerome Powell"

You: What is your view on current inflation?
Powell: The Federal Reserve remains committed to bringing
inflation back down to our 2 percent goal...

You: exit
```

### Verify System Status

```bash
python main.py status

# Output:
# Content items in database: 10
# Persona profile: Jerome Powell ✓
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
│   └── cli.py              # CLI interface
├── config/.env             # Configuration
├── data/database.db        # SQLite storage
├── main.py                 # Entry point
└── requirements.txt        # Dependencies
```

## Documentation

- **README.md** (this file): Quick start and Powell FOMC use case

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


