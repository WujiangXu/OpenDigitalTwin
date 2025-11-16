# Scenario-Based English Learning for CS PhD Students

A comprehensive role-play system designed specifically for international Computer Science PhD students in the USA. Practice real-world academic, social, and professional conversations through interactive scenarios.

## 🎯 Why Scenario-Based Learning?

Traditional English practice often lacks:
- **Context**: Real situations you'll actually face
- **Pressure**: Thinking on your feet in conversations
- **Cultural nuances**: American academic and social norms
- **Long-turn dialogue**: Sustained conversations, not just Q&A

Scenario-based learning addresses all of these!

## 📚 Available Scenario Categories

### 1. Academic Scenarios
**Perfect for**: Research discussions, presentations, teaching

| Scenario | Difficulty | Duration | You Practice |
|----------|------------|----------|--------------|
| **Office Hours** | Intermediate | 15 min | Meeting with advisor, discussing research progress |
| **Research Presentation** | Advanced | 20 min | Presenting at lab meeting, handling Q&A |
| **TA Duties** | Intermediate | 15 min | Helping undergrads, explaining concepts |

### 2. Campus Life Scenarios
**Perfect for**: Navigation, administration, daily tasks

| Scenario | Difficulty | Duration | You Practice |
|----------|------------|----------|--------------|
| **Course Registration** | Beginner | 10 min | Planning schedule with advisor |
| **Library Research** | Beginner | 10 min | Finding papers, using databases |

### 3. Social Scenarios
**Perfect for**: Making friends, networking, casual conversation

| Scenario | Difficulty | Duration | You Practice |
|----------|------------|----------|--------------|
| **Coffee Chat** | Intermediate | 15 min | Talking with senior PhD student |
| **Networking Event** | Intermediate | 12 min | Department reception, introductions |
| **Roommate Talk** | Beginner | 10 min | Everyday apartment conversations |

### 4. Professional Scenarios
**Perfect for**: Career development, networking, conferences

| Scenario | Difficulty | Duration | You Practice |
|----------|------------|----------|--------------|
| **Conference Networking** | Advanced | 15 min | Meeting researchers at NeurIPS/CVPR |
| **Research Collaboration** | Advanced | 15 min | Proposing collaboration via email/call |
| **Job Interview** | Advanced | 20 min | Research scientist interview |

### 5. Everyday Situations
**Perfect for**: Daily life in the USA

| Scenario | Difficulty | Duration | You Practice |
|----------|------------|----------|--------------|
| **Doctor's Appointment** | Intermediate | 10 min | Explaining symptoms, understanding advice |
| **Grocery Shopping** | Beginner | 8 min | Finding items, asking for help |

---

## 🚀 Quick Start

### List All Scenarios

```bash
# See all available scenarios
python main.py scenario --list

# Filter by category
python main.py scenario --list --category academic

# Filter by difficulty
python main.py scenario --list --difficulty beginner
```

### Start a Specific Scenario

```bash
# Start "Office Hours with Advisor"
python main.py scenario --scenario-id academic_office_hours

# Or use the shorthand
python main.py scenario -s academic_office_hours
```

### Interactive Selection

```bash
# Browse and select interactively
python main.py scenario

# Filter and then select
python main.py scenario --category social --difficulty intermediate
```

### Random Practice

```bash
# Random scenario from any category
python main.py scenario --random

# Random academic scenario
python main.py scenario --random --category academic
```

---

## 💡 How It Works

### 1. **Choose Your Scenario**

Each scenario includes:
- **Context**: Detailed situation setup
- **AI Role**: Character you'll interact with (e.g., Professor, classmate, librarian)
- **Learning Objectives**: Skills you'll practice
- **Vocabulary Focus**: Key phrases and terms
- **Cultural Notes**: American academic/social norms

### 2. **Immersive Role-Play**

The AI stays in character throughout the conversation:

```
📚 Scenario: Meeting with Your Advisor
🎯 Difficulty: intermediate | ⏱️ Duration: ~15 minutes

Situation:
You are meeting with your PhD advisor, Professor Sarah Chen, for weekly office hours.
You need to discuss your progress on the research project, ask for guidance on a technical
challenge, and get feedback on your upcoming conference paper draft.

You will interact with: Professor Sarah Chen
Supportive but busy, expects clear updates, asks probing questions

Learning Objectives:
  - Summarize research progress clearly and concisely
  - Ask technical questions professionally
  - Respond to critical feedback constructively
  - Negotiate deadlines and expectations

💡 Cultural Tips:
  • Office hours are your time - don't apologize for 'bothering' them
  • Speaking up in class is expected and valued
  • Deadlines are usually strict - ask for extensions early

Ready? Start the conversation whenever you're ready!
```

### 3. **Natural Conversation**

You can:
- **Speak** (press ENTER to record voice)
- **Type** (just type your message)
- **Check progress** (type `progress`)
- **End scenario** (type `end`)

### 4. **AI Responds in Character**

```
You: Hi Professor Chen, thanks for meeting with me today.
     I wanted to update you on the experiments I've been running.

🤖 Professor Sarah Chen: Of course! Have a seat. I'm glad you're here.
                         How are the experiments going? Last time we
                         talked, you were working on the baseline
                         comparisons, right?
```

### 5. **Review and Improve**

At the end, you get:
- **Performance summary**: Number of exchanges
- **Learning objectives covered**
- **Vocabulary practiced**
- **Conversation transcript** (saved automatically)

---

## 📖 Example Scenarios in Detail

### Academic: Office Hours

**Scenario ID**: `academic_office_hours`

**You'll practice:**
- Summarizing research progress concisely
- Asking for technical guidance
- Discussing experimental results
- Handling critical feedback
- Negotiating timelines

**Key vocabulary**:
- "preliminary results"
- "baseline comparison"
- "statistical significance"
- "methodology"
- "reproduce the results"

**Sample conversation starters**:
- "Hi Professor Chen, thanks for meeting with me today."
- "I wanted to update you on the experiments I've been running."
- "I've encountered a challenge with the implementation..."

---

### Social: Coffee Chat

**Scenario ID**: `social_coffee_chat`

**You'll practice:**
- Making small talk naturally
- Asking for advice informally
- Sharing your own experiences
- Building rapport

**Key vocabulary**:
- "work-life balance"
- "imposter syndrome"
- "qualifying exam"
- "How's it going?"
- "Any tips for...?"

**Sample conversation starters**:
- "Thanks for meeting up! How's your research going?"
- "I'm curious about your experience so far in the program."

---

### Professional: Conference Networking

**Scenario ID**: `prof_conference`

**You'll practice:**
- Introducing yourself to senior researchers
- Discussing research at technical level
- Asking insightful questions
- Exchanging contact information professionally

**Key vocabulary**:
- "I really enjoyed your talk on..."
- "Have you considered..."
- "My research is related..."
- "Would you be open to discussing..."

---

## 🎓 Recommended Learning Path

### Week 1: Survival Basics
Start with beginner scenarios to handle immediate needs:

```bash
python main.py scenario -s campus_registration
python main.py scenario -s campus_library
python main.py scenario -s social_roommate
python main.py scenario -s everyday_grocery
```

### First Month: Academic Essentials
Move to academic scenarios:

```bash
python main.py scenario -s academic_office_hours
python main.py scenario -s social_coffee_chat
python main.py scenario -s everyday_doctor
python main.py scenario -s academic_ta_duties
```

### First Semester: Advanced Skills
Tackle complex situations:

```bash
python main.py scenario -s academic_presentation
python main.py scenario -s social_networking
python main.py scenario -s prof_conference
```

### Advanced: Career Preparation
Practice high-stakes scenarios:

```bash
python main.py scenario -s prof_job_interview
python main.py scenario -s prof_collaboration_email
```

---

## 💬 Tips for Effective Practice

### Before the Scenario

1. **Read the context carefully** - Understand the situation
2. **Note the learning objectives** - Know what skills to focus on
3. **Review vocabulary list** - Familiar terms help confidence
4. **Check cultural notes** - Learn American norms

### During the Scenario

1. **Stay in character** - Pretend it's real
2. **Think before speaking** - Take time to formulate thoughts
3. **Use the vocabulary** - Try to incorporate key phrases
4. **Ask for clarification** - Just like you would in real life
5. **Don't worry about mistakes** - The AI models correct usage

### After the Scenario

1. **Review the transcript** - See what you said vs. AI responses
2. **Note new phrases** - What did the AI use that was good?
3. **Identify patterns** - What could you improve?
4. **Practice again** - Same scenario, better performance

---

## 🌍 Cultural Notes for International Students

### American Academic Culture

✅ **DO**:
- Call professors by first name (if they offer)
- Speak up in class - participation is valued
- Use office hours - they're your time
- Ask questions - shows engagement
- Collaborate - but understand plagiarism rules

❌ **DON'T**:
- Apologize for "bothering" professors
- Stay silent in discussions
- Wait for invitation to participate
- Pretend to understand if you don't
- Copy work without attribution

### Communication Style

**Direct vs. Indirect**:
- Americans often use indirect language: "Maybe you could consider..."
- This is polite, not weak
- You can be more direct than in many Asian cultures

**Small Talk**:
- Expected before business discussions
- "How was your weekend?" is normal
- Weather is always safe topic

**Saying "I don't know"**:
- Perfectly acceptable and professional
- Better than pretending to know
- Follow with "but I can find out"

### Social Norms

- **RSVP**: Always respond to invitations (yes or no)
- **Punctuality**: Arrive on time (or within 10 min)
- **Splitting bills**: Common among students ("go Dutch")
- **Personal space**: Keep about arm's length
- **"Let's grab coffee"**: Often means "let's talk", not always literal

---

## 🔧 Advanced Usage

### Custom Voice Selection

```bash
# Use different voices for different scenarios
python main.py scenario -s academic_office_hours --voice onyx  # Male
python main.py scenario -s social_coffee_chat --voice nova     # Female
```

### Filter by Multiple Criteria

```bash
# Beginner academic scenarios
python main.py scenario --list --category academic --difficulty beginner

# Advanced professional scenarios
python main.py scenario --list --category professional --difficulty advanced
```

### Search Scenarios

```python
from src.teacher.scenario_manager import ScenarioManager

mgr = ScenarioManager()

# Search by keyword
results = mgr.search_scenarios("presentation")
for scenario in results:
    print(f"{scenario.title}: {scenario.description}")
```

---

## 📊 Tracking Progress

### Automatic Saving

Every scenario conversation is saved to:
```
data/conversations/conversation_YYYYMMDD_HHMMSS.txt
```

### What's Saved:
- Full conversation transcript
- Scenario details
- Vocabulary practiced
- Learning objectives
- AI summary of conversation

### Review Your Progress:

```bash
# View recent conversations
ls -lt data/conversations/

# Read a specific conversation
cat data/conversations/conversation_20250115_143022.txt
```

---

## 🆘 Troubleshooting

### "Scenario not found"
```bash
# List available scenarios to get correct ID
python main.py scenario --list
```

### AI Breaking Character
- This shouldn't happen, but if it does:
- The scenario system uses specialized prompts
- Try a different scenario
- Check that you're using scenario command, not voice-chat

### Voice Not Working
- See main troubleshooting guide
- Make sure PyAudio is installed
- Check microphone permissions

---

## 🎯 Success Stories

### "The office hours scenario saved me"
*"I practiced 'academic_office_hours' three times before my first real meeting. When my advisor asked about my progress, I knew exactly how to structure my update. It was like I'd done it before!"*
— Wei, 1st year PhD

### "Networking is no longer scary"
*"The conference scenarios taught me how to approach senior researchers. I used the exact phrases at CVPR and ended up getting invited to a collaboration!"*
— Priya, 3rd year PhD

### "Cultural notes are gold"
*"I didn't know it was okay to call professors by first name. The cultural tips in the scenarios helped me understand American academic culture."*
— Jae, 1st year PhD

---

## 🚀 Next Features (Coming Soon)

- [ ] Progress tracking across sessions
- [ ] Personalized scenario recommendations
- [ ] More scenarios (qualifying exam, thesis defense)
- [ ] Multi-person conversations
- [ ] Pronunciation feedback
- [ ] Grammar explanations in context

---

## 📝 Creating Custom Scenarios

Want to add your own scenarios? Edit:
```
src/teacher/scenarios/cs_phd_scenarios.yaml
```

Follow the existing format:
```yaml
your_category:
  your_scenario:
    scenario_id: "your_scenario_id"
    title: "Your Scenario Title"
    difficulty: "intermediate"
    # ... (see existing scenarios for full structure)
```

---

## 💻 API Usage

### Programmatic Access

```python
from src.teacher.english_teacher import EnglishTeacher
from src.teacher.scenario_manager import ScenarioManager

# Initialize
teacher = EnglishTeacher()
mgr = ScenarioManager()

# List scenarios
scenarios = mgr.list_scenarios(category='academic')
for s in scenarios:
    print(f"{s.title} ({s.difficulty})")

# Start a scenario
intro = teacher.start_scenario('academic_office_hours')
print(intro)

# Have conversation
response = teacher.chat("Hi Professor, I want to discuss my research.")
print(response)

# Check progress
progress = teacher.get_scenario_progress()
print(f"Exchanges: {progress['exchanges_completed']}")

# End scenario
summary = teacher.end_scenario()
print(summary['conversation_summary'])
```

---

## 🤝 Contributing

Want to add more scenarios? Please submit PRs with:
- Realistic situations for CS PhD students
- Clear learning objectives
- Appropriate vocabulary
- Cultural notes where relevant

See `cs_phd_scenarios.yaml` for format.

---

## 📚 References

- [A-MEM Memory System](https://github.com/WujiangXu/A-mem-sys)
- [OpenAI Whisper](https://openai.com/research/whisper)
- [OpenAI TTS Documentation](https://platform.openai.com/docs/guides/text-to-speech)

---

**Happy Learning! 🎓**

Practice makes perfect. The more scenarios you complete, the more confident you'll become in real situations!
