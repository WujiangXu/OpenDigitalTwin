"""Unit tests for configuration management."""

import pytest
import os
from src.teacher.config import TeacherConfig, VoiceConfig


class TestTeacherConfig:
    """Test cases for TeacherConfig class."""

    def test_default_values(self):
        """Test default configuration values."""
        config = TeacherConfig()

        assert config.model == "gpt-4o"
        assert config.temperature == 0.7
        assert config.max_tokens == 300
        assert config.use_memory is True
        assert config.memory_dir == "data/teacher_memory"
        assert config.max_history_exchanges == 10
        assert config.memory_retrieval_top_k == 3

    def test_from_env_defaults(self, mock_env_vars):
        """Test creating config from environment with defaults."""
        config = TeacherConfig.from_env()

        assert config.model == "gpt-4o"
        assert isinstance(config.temperature, float)
        assert isinstance(config.max_tokens, int)

    def test_from_env_with_env_vars(self, monkeypatch):
        """Test creating config from environment variables."""
        monkeypatch.setenv("TEACHER_MODEL", "gpt-3.5-turbo")
        monkeypatch.setenv("TEACHER_TEMPERATURE", "0.5")
        monkeypatch.setenv("TEACHER_MAX_TOKENS", "500")
        monkeypatch.setenv("TEACHER_USE_MEMORY", "false")

        config = TeacherConfig.from_env()

        assert config.model == "gpt-3.5-turbo"
        assert config.temperature == 0.5
        assert config.max_tokens == 500
        assert config.use_memory is False

    def test_from_env_with_overrides(self):
        """Test creating config with override parameters."""
        config = TeacherConfig.from_env(
            model="custom-model",
            temperature=0.9,
            use_memory=False
        )

        assert config.model == "custom-model"
        assert config.temperature == 0.9
        assert config.use_memory is False

    def test_custom_initialization(self):
        """Test custom configuration initialization."""
        config = TeacherConfig(
            model="test-model",
            temperature=0.8,
            max_tokens=200,
            use_memory=False
        )

        assert config.model == "test-model"
        assert config.temperature == 0.8
        assert config.max_tokens == 200
        assert config.use_memory is False


class TestVoiceConfig:
    """Test cases for VoiceConfig class."""

    def test_default_values(self):
        """Test default configuration values."""
        config = VoiceConfig()

        assert config.stt_model == "whisper-1"
        assert config.stt_language == "en"
        assert config.tts_model == "tts-1"
        assert config.tts_voice == "nova"
        assert config.sample_rate == 16000
        assert config.channels == 1
        assert config.chunk_size == 1024

    def test_from_env_defaults(self):
        """Test creating config from environment with defaults."""
        config = VoiceConfig.from_env()

        assert config.stt_model == "whisper-1"
        assert config.tts_voice == "nova"

    def test_from_env_with_env_vars(self, monkeypatch):
        """Test creating config from environment variables."""
        monkeypatch.setenv("STT_MODEL", "whisper-2")
        monkeypatch.setenv("STT_LANGUAGE", "es")
        monkeypatch.setenv("TTS_MODEL", "tts-1-hd")
        monkeypatch.setenv("TTS_VOICE", "onyx")
        monkeypatch.setenv("AUDIO_SAMPLE_RATE", "48000")

        config = VoiceConfig.from_env()

        assert config.stt_model == "whisper-2"
        assert config.stt_language == "es"
        assert config.tts_model == "tts-1-hd"
        assert config.tts_voice == "onyx"
        assert config.sample_rate == 48000

    def test_from_env_with_overrides(self):
        """Test creating config with override parameters."""
        config = VoiceConfig.from_env(
            tts_voice="alloy",
            sample_rate=44100
        )

        assert config.tts_voice == "alloy"
        assert config.sample_rate == 44100

    def test_custom_initialization(self):
        """Test custom configuration initialization."""
        config = VoiceConfig(
            stt_model="custom-whisper",
            tts_voice="shimmer",
            sample_rate=22050
        )

        assert config.stt_model == "custom-whisper"
        assert config.tts_voice == "shimmer"
        assert config.sample_rate == 22050
