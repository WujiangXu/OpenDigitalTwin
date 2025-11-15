# 🎓 English Teaching Assistant

> A voice-enabled AI English teaching assistant for practicing conversational English

## Quick Start

```bash
# 1. Install dependencies (one-time setup)
brew install portaudio
pip3 install -r requirements.txt

# 2. Configure API key
cp config/.env.example config/.env
# Edit config/.env and add your OPENAI_API_KEY

# 3. Start chatting!
./english_teacher.sh

# Or use the full command:
python3 main.py voice-chat
```

## Features

✅ **Voice Conversation** - Speak and listen naturally
✅ **Smart AI Teacher** - GPT-4 powered adaptive responses
✅ **Conversation Memory** - Remembers your learning progress
✅ **Cost-Effective** - Only ~$5-10/month for daily practice
✅ **Mac Optimized** - Native macOS audio support

## Usage

```bash
# Default (female voice, with memory)
python3 main.py voice-chat

# Male voice
python3 main.py voice-chat --voice onyx

# Different voices
python3 main.py voice-chat --voice nova      # Female (default)
python3 main.py voice-chat --voice alloy     # Neutral
python3 main.py voice-chat --voice shimmer   # Female, warm

# Disable memory (fresh session)
python3 main.py voice-chat --no-memory
```

## How It Works

1. **Press ENTER** → Start recording
2. **Speak** → Talk in English
3. **Press ENTER** → Stop recording
4. **Listen** → AI responds with voice
5. **Repeat** → Keep practicing!

**Alternative**: Type your message instead of recording

## Cost Breakdown

| Service | Price | Daily (30min) | Monthly |
|---------|-------|---------------|---------|
| Whisper STT | $0.006/min | $0.18 | $5.40 |
| OpenAI TTS | $15/1M chars | $0.05 | $1.50 |
| GPT-4o Chat | Variable | $0.30 | $9.00 |
| **TOTAL** | - | **~$0.53** | **~$16** |

*Actual costs may vary based on conversation length and frequency*

## What You Can Practice

- 💬 Casual conversations about any topic
- 📚 Grammar explanations and corrections
- 🗣️ Natural pronunciation and listening
- 📝 Vocabulary building
- 🎯 Free talk practice

## Saved Conversations

All sessions are automatically saved to `data/conversations/` with:
- Full transcript
- Timestamp
- Session summary

```bash
# View your conversations
ls data/conversations/
cat data/conversations/conversation_20250115_143022.txt
```

## Requirements

- **macOS** 10.14+
- **Python** 3.8+
- **Microphone** (built-in or external)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Internet connection**

## Full Documentation

📖 See [docs/ENGLISH_TEACHER_SETUP.md](docs/ENGLISH_TEACHER_SETUP.md) for:
- Detailed installation guide
- Troubleshooting tips
- Privacy information
- Advanced usage

## Example Session

```
🎓 English Teaching Assistant - Voice Chat Mode

🤖 Teacher: Hello! I'm your English teaching assistant.
            What would you like to talk about today?

Press ENTER to record, or type your message: [ENTER]

🎤 Recording started... (Press ENTER when done)
[You speak: "I want to improve my English speaking skills."]
[ENTER]

👤 You said: I want to improve my English speaking skills.

🤖 Teacher: That's fantastic! Speaking practice is one of the
            best ways to improve. What topics are you most
            interested in discussing? I can help you practice
            conversations about work, hobbies, travel, or
            anything else you'd like!
```

## Troubleshooting

**PyAudio Error?**
```bash
brew install portaudio
pip install --upgrade pyaudio
```

**API Key Error?**
```bash
# Make sure config/.env has:
OPENAI_API_KEY=sk-your-key-here
```

**Microphone Not Working?**
- Check: System Preferences → Security & Privacy → Microphone
- Grant permission to Terminal/Python

## Commands During Chat

- `quit` or `exit` - End session and save
- `save` - Save conversation without exiting
- Type text - Skip voice recording

## Tips for Best Results

1. 🎯 Practice 15-30 minutes daily
2. 🔇 Use a quiet environment
3. 🎤 Speak clearly and naturally
4. 💬 Ask questions when confused
5. 📖 Review saved conversations

## Privacy

- Voice recordings are temporary (deleted after transcription)
- Conversations sent to OpenAI for processing
- Local storage: `data/teacher_memory/` and `data/conversations/`
- Delete data: `rm -rf data/teacher_memory/ data/conversations/`

## Support

For issues or questions:
1. Check [docs/ENGLISH_TEACHER_SETUP.md](docs/ENGLISH_TEACHER_SETUP.md)
2. Verify API key in `config/.env`
3. Ensure dependencies installed: `pip install -r requirements.txt`

---

**Happy Learning!** 🚀

Built with ❤️ using OpenAI Whisper, GPT-4, and TTS APIs
