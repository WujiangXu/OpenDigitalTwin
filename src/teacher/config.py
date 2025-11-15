"""Configuration management for English teaching assistant."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class TeacherConfig:
    """Configuration for English teaching assistant."""

    # LLM settings
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 300

    # Memory settings
    use_memory: bool = True
    memory_dir: str = "data/teacher_memory"
    conversation_dir: str = "data/conversations"

    # Context settings
    max_history_exchanges: int = 10  # Number of recent exchanges to keep in context
    memory_retrieval_top_k: int = 3  # Number of memories to retrieve

    # Session settings
    auto_save: bool = True

    @classmethod
    def from_env(cls, **overrides) -> 'TeacherConfig':
        """Create configuration from environment variables.

        Args:
            **overrides: Override specific configuration values

        Returns:
            TeacherConfig instance
        """
        config = cls(
            model=os.getenv('TEACHER_MODEL', cls.model),
            temperature=float(os.getenv('TEACHER_TEMPERATURE', cls.temperature)),
            max_tokens=int(os.getenv('TEACHER_MAX_TOKENS', cls.max_tokens)),
            use_memory=os.getenv('TEACHER_USE_MEMORY', str(cls.use_memory)).lower() == 'true',
            memory_dir=os.getenv('TEACHER_MEMORY_DIR', cls.memory_dir),
            conversation_dir=os.getenv('TEACHER_CONVERSATION_DIR', cls.conversation_dir),
        )

        # Apply overrides
        for key, value in overrides.items():
            if hasattr(config, key):
                setattr(config, key, value)

        return config


@dataclass
class VoiceConfig:
    """Configuration for voice interaction."""

    # Speech-to-text settings
    stt_model: str = "whisper-1"
    stt_language: str = "en"

    # Text-to-speech settings
    tts_model: str = "tts-1"  # or "tts-1-hd" for higher quality
    tts_voice: str = "nova"  # alloy, echo, fable, onyx, nova, shimmer

    # Audio recording settings
    sample_rate: int = 16000  # 16kHz is optimal for Whisper
    channels: int = 1  # Mono
    chunk_size: int = 1024

    @classmethod
    def from_env(cls, **overrides) -> 'VoiceConfig':
        """Create configuration from environment variables.

        Args:
            **overrides: Override specific configuration values

        Returns:
            VoiceConfig instance
        """
        config = cls(
            stt_model=os.getenv('STT_MODEL', cls.stt_model),
            stt_language=os.getenv('STT_LANGUAGE', cls.stt_language),
            tts_model=os.getenv('TTS_MODEL', cls.tts_model),
            tts_voice=os.getenv('TTS_VOICE', cls.tts_voice),
            sample_rate=int(os.getenv('AUDIO_SAMPLE_RATE', cls.sample_rate)),
            channels=int(os.getenv('AUDIO_CHANNELS', cls.channels)),
        )

        # Apply overrides
        for key, value in overrides.items():
            if hasattr(config, key):
                setattr(config, key, value)

        return config
