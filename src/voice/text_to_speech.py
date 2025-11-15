"""Text-to-speech module using OpenAI TTS API."""

import os
import tempfile
from openai import OpenAI
from typing import Optional, Literal
import subprocess
import platform


class TextToSpeech:
    """Converts text to speech using OpenAI TTS API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "tts-1",
        voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "nova"
    ):
        """Initialize the text-to-speech engine.

        Args:
            api_key: OpenAI API key (reads from OPENAI_API_KEY env var if not provided)
            model: TTS model to use ('tts-1' for faster/cheaper, 'tts-1-hd' for higher quality)
            voice: Voice to use (nova is female, onyx is male, alloy is neutral)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.voice = voice

    def speak(self, text: str, play_audio: bool = True) -> Optional[str]:
        """Convert text to speech and optionally play it.

        Args:
            text: Text to convert to speech
            play_audio: Whether to play the audio automatically

        Returns:
            Path to the audio file if play_audio is False, None otherwise
        """
        try:
            # Generate speech
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )

            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            temp_path = temp_file.name
            temp_file.close()

            # Save audio to file
            response.stream_to_file(temp_path)

            if play_audio:
                self._play_audio(temp_path)
                # Clean up after playing
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return None
            else:
                return temp_path

        except Exception as e:
            raise Exception(f"Text-to-speech conversion failed: {str(e)}")

    def _play_audio(self, audio_file_path: str):
        """Play audio file using system audio player.

        Args:
            audio_file_path: Path to the audio file
        """
        system = platform.system()

        try:
            if system == "Darwin":  # macOS
                subprocess.run(["afplay", audio_file_path], check=True)
            elif system == "Linux":
                # Try multiple players in order of preference
                players = ["mpg123", "ffplay", "aplay", "paplay"]
                for player in players:
                    try:
                        subprocess.run([player, audio_file_path], check=True,
                                     stderr=subprocess.DEVNULL)
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
            elif system == "Windows":
                import winsound
                winsound.PlaySound(audio_file_path, winsound.SND_FILENAME)
            else:
                print(f"⚠️  Auto-play not supported on {system}. Audio saved to: {audio_file_path}")

        except Exception as e:
            print(f"⚠️  Could not play audio: {str(e)}")
            print(f"Audio saved to: {audio_file_path}")

    def set_voice(self, voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]):
        """Change the voice.

        Args:
            voice: Voice name to use
        """
        self.voice = voice
        print(f"🔊 Voice changed to: {voice}")
