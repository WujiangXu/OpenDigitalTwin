# English Teaching Assistant - Setup Guide (Mac)

A voice-enabled AI English teaching assistant that helps you practice English through natural conversation.

## 🎯 Features

- **Voice Conversation**: Speak and listen to practice English naturally
- **Smart AI Teacher**: Uses GPT-4 to provide engaging, adaptive responses
- **Conversation Memory**: Remembers your progress across sessions
- **Cost-Effective**: Uses the cheapest reliable APIs (OpenAI Whisper + TTS)
- **Mac Optimized**: Native audio support for macOS

## 💰 Cost Estimate

For casual daily use (30 minutes/day):

| Service | Cost | Notes |
|---------|------|-------|
| **Whisper (Speech-to-Text)** | ~$0.18/session | $0.006/minute × 30 min |
| **TTS (Text-to-Speech)** | ~$0.05/session | ~3,000 characters @ $15/1M chars |
| **GPT-4o (Conversation)** | ~$0.30/session | Variable based on length |
| **TOTAL** | **~$5-10/month** | Based on 30 min/day usage |

## 📋 Prerequisites

### 1. macOS Requirements

- macOS 10.14 or later
- Microphone (built-in or external)
- Speakers/headphones
- Internet connection

### 2. Python Environment

```bash
# Check Python version (3.8+ required)
python3 --version
```

### 3. OpenAI API Key

1. Sign up at [OpenAI](https://platform.openai.com/)
2. Navigate to API Keys section
3. Create a new API key
4. Copy the key (starts with `sk-...`)

## 🚀 Installation

### Step 1: Install System Dependencies

```bash
# Install PortAudio (required for PyAudio)
brew install portaudio

# If you don't have Homebrew, install it first:
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Clone and Setup Project

```bash
# Navigate to the project
cd OpenDigitalTwin

# Install Python dependencies
pip3 install -r requirements.txt

# Or use a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure API Key

```bash
# Copy example config
cp config/.env.example config/.env

# Edit the config file
nano config/.env  # or use any text editor

# Add your OpenAI API key:
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
```

### Step 4: Test Installation

```bash
# Test that everything is installed correctly
python3 main.py --help

# You should see the voice-chat command listed
```

## 🎤 Usage

### Basic Usage

```bash
# Start the voice chat with default settings (female voice)
python3 main.py voice-chat
```

### Advanced Options

```bash
# Use a different voice (male voice)
python3 main.py voice-chat --voice onyx

# All available voices:
# - nova (female, default)
# - alloy (neutral)
# - echo (male)
# - fable (male, expressive)
# - onyx (male, deep)
# - shimmer (female, warm)

# Disable conversation memory (fresh start each time)
python3 main.py voice-chat --no-memory
```

### During Conversation

1. **Press ENTER** to start recording
2. **Speak your message** in English
3. **Press ENTER** again to stop recording
4. **Listen to the response**
5. Repeat!

**Alternative**: You can also type your message instead of recording

**Commands**:
- Type `quit` or `exit` to end the session
- Type `save` to save the conversation without exiting

### Conversation Tips

- Speak naturally at a normal pace
- Wait for the teacher to finish speaking before responding
- Don't worry about mistakes - the AI will help you improve
- Ask for grammar explanations if you're confused
- Talk about topics that interest you!

## 📁 File Structure

```
OpenDigitalTwin/
├── src/
│   ├── voice/                    # Voice interaction modules
│   │   ├── audio_recorder.py     # Microphone recording
│   │   ├── speech_to_text.py     # Whisper integration
│   │   └── text_to_speech.py     # OpenAI TTS
│   ├── teacher/                  # English teaching logic
│   │   └── english_teacher.py    # Main teacher AI
│   └── cli.py                    # Command-line interface
├── data/
│   ├── teacher_memory/           # Conversation memory (created automatically)
│   └── conversations/            # Saved conversation logs
├── config/
│   └── .env                      # API configuration
└── requirements.txt              # Python dependencies
```

## 🔧 Troubleshooting

### "PyAudio not found" Error

```bash
# Make sure PortAudio is installed first
brew install portaudio

# Then reinstall PyAudio
pip install --upgrade pyaudio
```

### "OpenAI API key required" Error

```bash
# Check if .env file exists
cat config/.env

# Make sure OPENAI_API_KEY is set correctly
# Key should start with "sk-"
```

### Microphone Not Working

```bash
# Check microphone permissions:
# System Preferences > Security & Privacy > Microphone
# Make sure Terminal (or your Python app) has microphone access
```

### Audio Playback Issues

The assistant uses `afplay` on macOS which should work by default. If you have issues:

```bash
# Test audio playback manually
afplay /System/Library/Sounds/Ping.aiff

# Make sure volume is not muted
```

### Poor Transcription Quality

- Speak clearly and at a moderate pace
- Reduce background noise
- Use a better microphone if possible
- Make sure you're close enough to the microphone

## 💡 Tips for Best Results

### Getting Started

1. **Start Simple**: Begin with basic conversations about daily topics
2. **Be Patient**: The AI needs a moment to transcribe and respond
3. **Speak Clearly**: Especially if English isn't your first language
4. **Use Good Audio**: A quiet environment helps transcription accuracy

### Maximizing Learning

1. **Practice Regularly**: Even 15 minutes daily is better than occasional long sessions
2. **Ask Questions**: Request explanations when you don't understand
3. **Review Sessions**: Check saved conversations to see your progress
4. **Vary Topics**: Talk about different subjects to expand vocabulary
5. **Note Corrections**: The AI gently corrects by using correct forms in responses

### Cost Optimization

1. **Keep Sessions Focused**: 15-30 minutes is optimal for learning and cost
2. **Use Memory Feature**: It remembers context, so you don't need to repeat yourself
3. **Type When Possible**: Text input skips STT cost (useful for quick questions)

## 📊 Conversation History

All conversations are automatically saved to `data/conversations/` with:
- Full transcript
- Timestamp
- Automatic summary

```bash
# View saved conversations
ls -la data/conversations/

# Read a conversation
cat data/conversations/conversation_20250115_143022.txt
```

## 🔐 Privacy & Data

- **Voice recordings** are temporarily stored and immediately deleted after transcription
- **Conversations** are sent to OpenAI for processing (see [OpenAI Privacy Policy](https://openai.com/privacy))
- **Local storage** contains conversation history in `data/` directory
- **Memory system** stores conversation summaries locally in `data/teacher_memory/`

To delete all data:
```bash
rm -rf data/teacher_memory/
rm -rf data/conversations/
```

## 📚 What You Can Practice

- **Casual Conversation**: Daily life, hobbies, interests
- **Grammar Questions**: "When do I use 'have been' vs 'had been'?"
- **Vocabulary Building**: Discuss new topics to learn new words
- **Pronunciation**: Speak and get natural responses
- **Listening Comprehension**: Listen to the AI's natural speech
- **Free Talk**: Just chat about anything!

## 🆘 Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Verify API key is correct in `config/.env`
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Check microphone permissions in System Preferences

## 🔄 Updates

To update the assistant:

```bash
cd OpenDigitalTwin
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📝 Example Session

```
$ python3 main.py voice-chat

============================================================
🎓 English Teaching Assistant - Voice Chat Mode
============================================================

⚙️  Initializing...
✓ Teacher initialized
✓ Voice: nova
✓ Memory: Enabled

------------------------------------------------------------
📋 Instructions:
  1. Press ENTER to start recording
  2. Speak your message in English
  3. Press ENTER again to stop and send
  4. Type 'quit', 'exit', or 'save' to end
------------------------------------------------------------

🤖 Teacher: Hello! I'm your English teaching assistant...

Press ENTER to record, or type your message: [Press ENTER]

🎤 Recording started... (Press ENTER when done)
[You speak: "Hello! I want to practice English today."]
[Press ENTER]

🔄 Transcribing...
👤 You said: Hello! I want to practice English today.

💭 Thinking...

🤖 Teacher: That's wonderful! I'm so glad you're here to practice...
```

## 🎯 Next Steps

1. Install the system (follow installation steps above)
2. Start with a simple conversation
3. Practice for 15-30 minutes daily
4. Review your saved conversations
5. Track your progress over time

Happy learning! 🚀
