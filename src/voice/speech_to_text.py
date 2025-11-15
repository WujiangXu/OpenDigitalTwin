"""Speech-to-text module using OpenAI Whisper API."""

import os
from openai import OpenAI
from typing import Optional


class SpeechToText:
    """Converts speech to text using OpenAI Whisper API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "whisper-1"):
        """Initialize the speech-to-text engine.

        Args:
            api_key: OpenAI API key (reads from OPENAI_API_KEY env var if not provided)
            model: Whisper model to use (default: whisper-1)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def transcribe(self, audio_file_path: str, language: str = "en") -> str:
        """Transcribe audio file to text.

        Args:
            audio_file_path: Path to the audio file
            language: Language code (default: 'en' for English)

        Returns:
            Transcribed text

        Raises:
            Exception: If transcription fails
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=language,
                    response_format="text"
                )

            # Clean up the temporary file
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

            return transcript.strip()

        except Exception as e:
            # Clean up on error
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            raise Exception(f"Speech-to-text transcription failed: {str(e)}")

    def transcribe_with_timestamps(self, audio_file_path: str, language: str = "en") -> dict:
        """Transcribe audio with word-level timestamps.

        Args:
            audio_file_path: Path to the audio file
            language: Language code (default: 'en' for English)

        Returns:
            Dictionary with transcript and timing information
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=language,
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )

            # Clean up the temporary file
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

            return transcript

        except Exception as e:
            # Clean up on error
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            raise Exception(f"Speech-to-text transcription failed: {str(e)}")
