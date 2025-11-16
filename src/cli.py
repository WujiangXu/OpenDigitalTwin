"""
Command-line interface for OpenDigitalTwin.
"""
import click
import json
import os
from dotenv import load_dotenv

from extractor.extractor_factory import create_extractor, get_extractor_info
from extractor.document_parser import DocumentParser
from extractor.storage import Storage
from persona.analyzer import PersonaAnalyzer
from persona.generator import ResponseGenerator
from persona.llm_client import LLMClient
from teacher.english_teacher import EnglishTeacher
from teacher.scenario_manager import ScenarioManager
from voice.audio_recorder import AudioRecorder
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import TextToSpeech

# Load environment variables
load_dotenv('config/.env')


@click.group()
def cli():
    """OpenDigitalTwin - Build AI digital twins from extracted data."""
    pass


@cli.command()
@click.option('--type', '-t', 'extractor_type',
              type=click.Choice(['jina', 'firecrawl']),
              help='Extractor type to use')
def info(extractor_type):
    """Show information about available extractors."""
    extractors = get_extractor_info()

    if extractor_type:
        info_dict = extractors.get(extractor_type)
        if info_dict:
            click.echo(f"\n{info_dict['name']}")
            click.echo("=" * 50)
            click.echo(f"Cost: {info_dict['cost']}")
            click.echo(f"API Key Required: {info_dict['api_key_required']}")
            click.echo(f"Recommended For: {info_dict['recommended_for']}")
            click.echo(f"\nFeatures:")
            for feature in info_dict['features']:
                click.echo(f"  - {feature}")
    else:
        click.echo("\nAvailable Extractors:")
        click.echo("=" * 50)
        for key, info_dict in extractors.items():
            click.echo(f"\n{key.upper()}: {info_dict['name']}")
            click.echo(f"  Cost: {info_dict['cost']}")
            click.echo(f"  API Key: {'Required' if info_dict['api_key_required'] else 'Optional'}")


@cli.command()
@click.option('--url', '-u', multiple=True, help='URL to extract content from')
@click.option('--file', '-f', multiple=True, type=click.Path(exists=True),
              help='Local file to parse')
@click.option('--powell', is_flag=True, help='Extract Powell speeches automatically')
@click.option('--num', '-n', default=10, help='Number of Powell speeches to extract')
@click.option('--extractor', '-e', type=click.Choice(['jina', 'firecrawl']),
              help='Extractor to use (overrides config)')
def extract(url, file, powell, num, extractor):
    """Extract content from URLs or files and store in database."""
    storage = Storage()

    # Create extractor
    try:
        ext = create_extractor(extractor)
        click.echo(f"Using extractor: {extractor or os.getenv('EXTRACTOR_TYPE', 'jina')}")
    except Exception as e:
        click.echo(f"Error creating extractor: {e}", err=True)
        return

    extracted_items = []

    # Extract from URLs
    if url:
        click.echo(f"\nExtracting {len(url)} URLs...")
        for u in url:
            try:
                result = ext.extract_url(u)
                extracted_items.append(result)
                click.echo(f"✓ Extracted: {result['title']}")
            except Exception as e:
                click.echo(f"✗ Error extracting {u}: {e}", err=True)

    # Parse local files
    if file:
        parser = DocumentParser()
        click.echo(f"\nParsing {len(file)} files...")
        for f in file:
            try:
                result = parser.parse_file(f)
                extracted_items.append(result)
                click.echo(f"✓ Parsed: {result['title']}")
            except Exception as e:
                click.echo(f"✗ Error parsing {f}: {e}", err=True)

    # Extract Powell speeches
    if powell:
        click.echo(f"\nExtracting {num} Powell speeches...")
        try:
            results = ext.extract_powell_speeches(num)
            extracted_items.extend(results)
            click.echo(f"✓ Extracted {len(results)} speeches")
        except Exception as e:
            click.echo(f"✗ Error extracting Powell speeches: {e}", err=True)

    # Save to database
    if extracted_items:
        click.echo(f"\nSaving {len(extracted_items)} items to database...")
        for item in extracted_items:
            storage.add_content(
                source=item['url'],
                source_type=item['source_type'],
                content=item['content'],
                metadata=json.dumps({'title': item['title']})
            )
        click.echo(f"✓ Saved {len(extracted_items)} items")
        click.echo(f"\nTotal content items in database: {storage.get_content_count()}")
    else:
        click.echo("\nNo content extracted. Use --url, --file, or --powell options.")


@cli.command()
@click.option('--name', '-n', default='Jerome Powell', help='Name of person for persona')
def analyze(name):
    """Analyze extracted content and build persona profile."""
    storage = Storage()
    content_items = storage.get_all_content()

    if not content_items:
        click.echo("No content found in database. Run 'extract' command first.", err=True)
        return

    click.echo(f"\nAnalyzing {len(content_items)} content items for {name}...")

    try:
        analyzer = PersonaAnalyzer()
        persona = analyzer.analyze_content(content_items)

        # Save persona profile
        storage.save_persona_profile(name, json.dumps(persona, indent=2))

        click.echo(f"\n✓ Persona profile created for {name}")
        click.echo("\nPersona Summary:")
        click.echo("=" * 50)
        click.echo(f"\nWriting Style:\n{persona['writing_style']}")
        click.echo(f"\nCommunication Patterns:\n{persona['communication_patterns']}")
        click.echo(f"\nKey Topics:\n{persona['topics_themes']}")
        click.echo(f"\nDecision Style:\n{persona['decision_style']}")

    except Exception as e:
        click.echo(f"Error analyzing content: {e}", err=True)


@cli.command()
@click.argument('query')
@click.option('--name', '-n', default='Jerome Powell', help='Name of persona to use')
def query(query, name):
    """Ask a question to the digital twin."""
    storage = Storage()

    # Load persona profile
    profile = storage.get_persona_profile(name)
    if not profile:
        click.echo(f"No persona profile found for {name}. Run 'analyze' command first.", err=True)
        return

    persona = json.loads(profile['analysis'])

    try:
        # Create system prompt
        analyzer = PersonaAnalyzer()
        system_prompt = analyzer.create_system_prompt(persona, name)

        # Generate response
        generator = ResponseGenerator()
        context = generator.find_relevant_context(query)

        click.echo(f"\nGenerating response from {name}...\n")

        response = generator.generate_response(query, system_prompt, context)

        click.echo(f"{name}:")
        click.echo("-" * 50)
        click.echo(response)

    except Exception as e:
        click.echo(f"Error generating response: {e}", err=True)


@cli.command()
@click.option('--name', '-n', default='Jerome Powell', help='Name of persona to use')
def chat(name):
    """Interactive chat mode with the digital twin."""
    storage = Storage()

    # Load persona profile
    profile = storage.get_persona_profile(name)
    if not profile:
        click.echo(f"No persona profile found for {name}. Run 'analyze' command first.", err=True)
        return

    persona = json.loads(profile['analysis'])

    # Create system prompt
    analyzer = PersonaAnalyzer()
    system_prompt = analyzer.create_system_prompt(persona, name)

    generator = ResponseGenerator()

    click.echo(f"\n{'='*50}")
    click.echo(f"Chat with {name}")
    click.echo(f"{'='*50}")
    click.echo("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        try:
            user_input = click.prompt("You", type=str)

            if user_input.lower() in ['exit', 'quit']:
                click.echo("Goodbye!")
                break

            # Find relevant context
            context = generator.find_relevant_context(user_input)

            # Generate response
            response = generator.generate_response(user_input, system_prompt, context)

            click.echo(f"\n{name}:")
            click.echo(response)
            click.echo()

        except (KeyboardInterrupt, EOFError):
            click.echo("\nGoodbye!")
            break
        except Exception as e:
            click.echo(f"Error: {e}", err=True)


@cli.command()
@click.option('--inflation', default='3.2%', help='Current inflation rate')
@click.option('--unemployment', default='3.7%', help='Unemployment rate')
@click.option('--gdp-growth', default='2.5%', help='GDP growth rate')
@click.option('--name', '-n', default='Jerome Powell', help='Name of persona to use')
def fomc(inflation, unemployment, gdp_growth, name):
    """Generate an FOMC decision based on economic data."""
    storage = Storage()

    # Load persona profile
    profile = storage.get_persona_profile(name)
    if not profile:
        click.echo(f"No persona profile found for {name}. Run 'analyze' command first.", err=True)
        return

    persona = json.loads(profile['analysis'])

    # Prepare economic data
    economic_data = {
        'Inflation (CPI)': inflation,
        'Unemployment Rate': unemployment,
        'GDP Growth': gdp_growth,
        'Federal Funds Rate (current)': '5.25-5.50%',  # Example
    }

    try:
        # Create system prompt
        analyzer = PersonaAnalyzer()
        system_prompt = analyzer.create_system_prompt(persona, name)

        # Generate FOMC decision
        generator = ResponseGenerator()

        click.echo(f"\nGenerating FOMC decision as {name}...\n")

        decision = generator.generate_fomc_decision(economic_data, system_prompt)

        click.echo("=" * 60)
        click.echo("FOMC DECISION STATEMENT")
        click.echo("=" * 60)
        click.echo(decision)

    except Exception as e:
        click.echo(f"Error generating FOMC decision: {e}", err=True)


@cli.command()
def status():
    """Show current status of the digital twin."""
    storage = Storage()

    click.echo("\nOpenDigitalTwin Status")
    click.echo("=" * 50)

    # Content stats
    content_count = storage.get_content_count()
    click.echo(f"Content items in database: {content_count}")

    # Persona profiles
    # Simple check - try to load Powell profile
    profile = storage.get_persona_profile('Jerome Powell')
    if profile:
        click.echo(f"Persona profile: Jerome Powell ✓")
    else:
        click.echo(f"Persona profile: Not created")

    # Config
    extractor_type = os.getenv('EXTRACTOR_TYPE', 'jina')
    llm_provider = os.getenv('LLM_PROVIDER', 'openai')
    click.echo(f"\nConfiguration:")
    click.echo(f"  Extractor: {extractor_type}")
    click.echo(f"  LLM Provider: {llm_provider}")


@cli.command()
@click.option('--voice', '-v',
              type=click.Choice(['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']),
              default='nova',
              help='Voice to use for text-to-speech (nova=female, onyx=male)')
@click.option('--no-memory', is_flag=True, help='Disable conversation memory')
def voice_chat(voice, no_memory):
    """Voice-enabled English teaching assistant (Mac optimized).

    Press Enter to start/stop recording. Type 'quit' or 'exit' to end.
    """
    try:
        # Initialize components
        click.echo("\n" + "="*60)
        click.echo("🎓 English Teaching Assistant - Voice Chat Mode")
        click.echo("="*60)
        click.echo("\n⚙️  Initializing...")

        teacher = EnglishTeacher(use_memory=not no_memory)
        stt = SpeechToText()
        tts = TextToSpeech(voice=voice)
        recorder = AudioRecorder()

        click.echo(f"✓ Teacher initialized")
        click.echo(f"✓ Voice: {voice}")
        click.echo(f"✓ Memory: {'Disabled' if no_memory else 'Enabled'}")

        # Show instructions
        click.echo("\n" + "-"*60)
        click.echo("📋 Instructions:")
        click.echo("  1. Press ENTER to start recording")
        click.echo("  2. Speak your message in English")
        click.echo("  3. Press ENTER again to stop and send")
        click.echo("  4. Type 'quit', 'exit', or 'save' to end")
        click.echo("-"*60 + "\n")

        # Start conversation with greeting
        greeting = teacher.get_greeting()
        click.echo(f"🤖 Teacher: {greeting}\n")
        tts.speak(greeting)

        # Main conversation loop
        while True:
            try:
                # Check if user wants to type instead
                user_input = click.prompt(
                    "\nPress ENTER to record, or type your message",
                    type=str,
                    default="",
                    show_default=False
                )

                if user_input.lower() in ['quit', 'exit']:
                    # Save conversation before exiting
                    click.echo("\n💾 Saving conversation...")
                    teacher.save_session()
                    click.echo("\n👋 Goodbye! Keep practicing your English!")
                    break

                elif user_input.lower() == 'save':
                    teacher.save_session()
                    click.echo("Type 'quit' to exit or press ENTER to continue...")
                    continue

                # If user typed something, use that
                if user_input.strip():
                    student_message = user_input
                    click.echo(f"👤 You (typed): {student_message}")

                else:
                    # Record audio
                    click.echo("\n🎤 Recording started... (Press ENTER when done)")
                    audio_file = recorder.record_until_enter()

                    # Transcribe
                    click.echo("🔄 Transcribing...")
                    student_message = stt.transcribe(audio_file)
                    click.echo(f"👤 You said: {student_message}")

                # Check for exit commands in transcription
                if student_message.lower().strip() in ['quit', 'exit', 'goodbye', 'bye']:
                    click.echo("\n💾 Saving conversation...")
                    teacher.save_session()
                    response = "Goodbye! It was great practicing English with you. Keep up the good work!"
                    click.echo(f"\n🤖 Teacher: {response}\n")
                    tts.speak(response)
                    break

                # Generate response
                click.echo("💭 Thinking...")
                response = teacher.chat(student_message)

                # Display and speak response
                click.echo(f"\n🤖 Teacher: {response}\n")
                tts.speak(response)

            except KeyboardInterrupt:
                click.echo("\n\n⚠️  Interrupted. Saving conversation...")
                teacher.save_session()
                click.echo("👋 Goodbye!")
                break

            except Exception as e:
                click.echo(f"\n⚠️  Error: {str(e)}", err=True)
                click.echo("Let's try again...\n")

    except Exception as e:
        click.echo(f"\n❌ Failed to initialize: {str(e)}", err=True)
        click.echo("\nMake sure you have:")
        click.echo("  - OPENAI_API_KEY set in config/.env")
        click.echo("  - PyAudio installed (brew install portaudio && pip install pyaudio)")
        return

    finally:
        # Cleanup
        if 'recorder' in locals():
            recorder.cleanup()


@cli.command()
@click.option('--list', 'list_scenarios', is_flag=True, help='List available scenarios')
@click.option('--category', '-c', help='Filter by category (academic, social, professional, etc.)')
@click.option('--difficulty', '-d', type=click.Choice(['beginner', 'intermediate', 'advanced']),
              help='Filter by difficulty level')
@click.option('--scenario-id', '-s', help='Specific scenario ID to practice')
@click.option('--random', 'use_random', is_flag=True, help='Start a random scenario')
@click.option('--voice', '-v',
              type=click.Choice(['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']),
              default='nova', help='Voice for text-to-speech')
def scenario(list_scenarios, category, difficulty, scenario_id, use_random, voice):
    """Practice English with scenario-based role-play conversations.

    Designed for CS PhD students - practice academic, social, and professional situations.
    """
    try:
        # Initialize scenario manager
        scenario_mgr = ScenarioManager()

        # List scenarios if requested
        if list_scenarios:
            scenarios = scenario_mgr.list_scenarios(
                category=category,
                difficulty=difficulty
            )

            if not scenarios:
                click.echo("No scenarios found matching criteria.")
                return

            # Group by category
            by_category = {}
            for s in scenarios:
                if s.category not in by_category:
                    by_category[s.category] = []
                by_category[s.category].append(s)

            click.echo("\n" + "=" * 70)
            click.echo("📚 Available Scenarios for CS PhD Students")
            click.echo("=" * 70)

            for cat, scens in sorted(by_category.items()):
                click.echo(f"\n{cat.upper().replace('_', ' ')}:")
                click.echo("-" * 70)
                for s in scens:
                    click.echo(f"  [{s.difficulty}] {s.scenario_id}")
                    click.echo(f"    {s.title}")
                    click.echo(f"    {s.description}")
                    click.echo(f"    Duration: ~{s.duration_minutes} min | Role: {s.ai_role['name']}")
                    click.echo()

            # Show statistics
            stats = scenario_mgr.get_statistics()
            click.echo("=" * 70)
            click.echo(f"Total scenarios: {stats['total_scenarios']}")
            click.echo(f"Difficulties: {dict(stats['by_difficulty'])}")

            return

        # Select scenario
        selected_scenario = None

        if scenario_id:
            selected_scenario = scenario_mgr.get_scenario(scenario_id)
            if not selected_scenario:
                click.echo(f"Error: Scenario '{scenario_id}' not found.")
                click.echo("Use --list to see available scenarios.")
                return

        elif use_random:
            selected_scenario = scenario_mgr.get_random_scenario(
                category=category,
                difficulty=difficulty
            )

        else:
            # Interactive selection
            scenarios = scenario_mgr.list_scenarios(
                category=category,
                difficulty=difficulty
            )

            if not scenarios:
                click.echo("No scenarios available. Try different filters.")
                return

            click.echo("\nAvailable Scenarios:")
            for i, s in enumerate(scenarios, 1):
                click.echo(f"{i}. [{s.difficulty}] {s.title}")

            choice = click.prompt("\nSelect a scenario (number)", type=int)

            if 1 <= choice <= len(scenarios):
                selected_scenario = scenarios[choice - 1]
            else:
                click.echo("Invalid selection.")
                return

        # Initialize teacher and voice components
        click.echo("\n⚙️  Initializing scenario practice...")

        teacher = EnglishTeacher()
        stt = SpeechToText()
        tts = TextToSpeech(voice=voice)
        recorder = AudioRecorder()

        # Start the scenario
        intro_message = teacher.start_scenario(selected_scenario.scenario_id)

        click.echo("\n" + intro_message)

        # Show cultural notes if academic/professional
        if selected_scenario.category in ['academic', 'professional']:
            notes = scenario_mgr.get_cultural_notes('american_academic_culture')
            if notes and 'american_academic_culture' in notes:
                click.echo("\n💡 Cultural Tips:")
                for note in notes['american_academic_culture'][:3]:
                    click.echo(f"  • {note}")

        click.echo("\n" + "-" * 70)
        click.echo("🎤 Press ENTER to start speaking (or type your message)")
        click.echo("   Type 'end' to finish the scenario and see summary")
        click.echo("   Type 'progress' to see your progress")
        click.echo("-" * 70 + "\n")

        # Conversation loop
        while True:
            try:
                # Get user input (voice or text)
                user_input = click.prompt(
                    f"\n[{selected_scenario.ai_role['name']}] Press ENTER to record or type",
                    type=str,
                    default="",
                    show_default=False
                )

                if user_input.lower() == 'end':
                    # End scenario and show summary
                    summary = teacher.end_scenario()

                    click.echo("\n" + "=" * 70)
                    click.echo(f"✅ Scenario Completed: {summary['scenario']}")
                    click.echo("=" * 70)
                    click.echo(f"\n📊 Performance:")
                    click.echo(f"  • Conversation exchanges: {summary['duration']}")
                    click.echo(f"\n🎯 Learning Objectives Covered:")
                    for obj in summary['learning_objectives']:
                        click.echo(f"  ✓ {obj}")
                    click.echo(f"\n📚 Vocabulary Practiced:")
                    click.echo(f"  {', '.join(summary['vocabulary_practiced'][:10])}")
                    if len(summary['vocabulary_practiced']) > 10:
                        click.echo(f"  ... and {len(summary['vocabulary_practiced']) - 10} more")
                    click.echo(f"\n📝 Conversation Summary:")
                    click.echo(f"  {summary['conversation_summary']}")

                    # Save
                    filepath = teacher.save_session()
                    click.echo(f"\n💾 Session saved to: {filepath}")

                    break

                elif user_input.lower() == 'progress':
                    progress = teacher.get_scenario_progress()
                    if progress:
                        click.echo(f"\n📈 Progress:")
                        click.echo(f"  • Scenario: {progress['scenario']}")
                        click.echo(f"  • Exchanges: {progress['exchanges_completed']}")
                        click.echo(f"  • Estimated duration: {progress['estimated_duration_minutes']} min")
                        click.echo(f"  • Speaking with: {progress['ai_character']}")
                    continue

                # Get user message
                if user_input.strip():
                    student_message = user_input
                    click.echo(f"👤 You: {student_message}")
                else:
                    # Record audio
                    click.echo("\n🎤 Recording... (Press ENTER when done)")
                    audio_file = recorder.record_until_enter()

                    click.echo("🔄 Transcribing...")
                    student_message = stt.transcribe(audio_file)
                    click.echo(f"👤 You said: {student_message}")

                # Generate AI response
                click.echo("💭 Thinking...")
                response = teacher.chat(student_message)

                # Display and speak
                click.echo(f"\n🤖 {selected_scenario.ai_role['name']}: {response}\n")
                tts.speak(response)

            except KeyboardInterrupt:
                click.echo("\n\n⚠️  Scenario interrupted.")
                teacher.end_scenario()
                break

            except Exception as e:
                click.echo(f"\n⚠️  Error: {str(e)}")
                click.echo("Let's try again...\n")

    except Exception as e:
        click.echo(f"\n❌ Failed to initialize: {str(e)}")
        return

    finally:
        if 'recorder' in locals():
            recorder.cleanup()


if __name__ == '__main__':
    cli()
