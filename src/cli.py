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


if __name__ == '__main__':
    cli()
