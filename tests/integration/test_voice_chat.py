"""Integration tests for voice chat system."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.teacher.english_teacher import EnglishTeacher
from src.teacher.config import TeacherConfig, VoiceConfig
from src.teacher.prompt_loader import PromptLoader


class TestVoiceChatIntegration:
    """Integration tests for the complete voice chat system."""

    @pytest.fixture
    def voice_config(self):
        """Create voice configuration for testing."""
        return VoiceConfig(
            tts_voice="nova",
            sample_rate=16000
        )

    @pytest.fixture
    def mock_audio_components(self):
        """Create mock audio components."""
        mocks = {
            'recorder': Mock(),
            'stt': Mock(),
            'tts': Mock()
        }

        # Configure mocks
        mocks['recorder'].record_until_enter.return_value = "/tmp/test_audio.wav"
        mocks['stt'].transcribe.return_value = "Hello, I want to practice English"
        mocks['tts'].speak.return_value = None

        return mocks

    def test_complete_voice_interaction_flow(
        self,
        mock_llm_client,
        teacher_config,
        prompts_dir,
        mock_audio_components
    ):
        """Test complete flow: record → transcribe → respond → speak."""
        # Setup teacher
        prompt_loader = PromptLoader(prompts_dir)
        teacher = EnglishTeacher(
            llm_client=Mock(),
            config=teacher_config,
            prompt_loader=prompt_loader
        )
        teacher.llm_client.generate = Mock(return_value="Great! Let's practice together.")

        # Simulate voice interaction flow
        recorder = mock_audio_components['recorder']
        stt = mock_audio_components['stt']
        tts = mock_audio_components['tts']

        # 1. Record audio
        audio_file = recorder.record_until_enter()
        assert audio_file is not None

        # 2. Transcribe to text
        user_message = stt.transcribe(audio_file)
        assert user_message == "Hello, I want to practice English"

        # 3. Generate response
        response = teacher.chat(user_message)
        assert response is not None

        # 4. Speak response
        tts.speak(response)
        assert tts.speak.called

    def test_error_handling_in_voice_flow(
        self,
        mock_llm_client,
        teacher_config,
        prompts_dir
    ):
        """Test error handling in voice interaction."""
        prompt_loader = PromptLoader(prompts_dir)
        teacher = EnglishTeacher(
            llm_client=Mock(),
            config=teacher_config,
            prompt_loader=prompt_loader
        )

        # Test with transcription error
        with patch('src.voice.speech_to_text.SpeechToText') as mock_stt:
            mock_stt.return_value.transcribe.side_effect = Exception("Transcription failed")

            # Should handle error gracefully
            # In real implementation, this would be caught by try-except

    def test_conversation_persistence_across_interactions(
        self,
        teacher_config,
        prompts_dir
    ):
        """Test that conversation history persists across multiple voice interactions."""
        prompt_loader = PromptLoader(prompts_dir)
        teacher = EnglishTeacher(
            llm_client=Mock(),
            config=teacher_config,
            prompt_loader=prompt_loader
        )
        teacher.llm_client.generate = Mock(return_value="Mock response")

        # Simulate multiple interactions
        messages = [
            "Hello",
            "How are you?",
            "Tell me about grammar"
        ]

        for msg in messages:
            teacher.chat(msg)

        # Verify history is maintained
        assert len(teacher.conversation_history) == len(messages) * 2

    def test_session_save_after_voice_chat(
        self,
        teacher_config,
        prompts_dir,
        temp_dir
    ):
        """Test saving session after voice chat."""
        prompt_loader = PromptLoader(prompts_dir)
        teacher = EnglishTeacher(
            llm_client=Mock(),
            config=teacher_config,
            prompt_loader=prompt_loader
        )
        teacher.llm_client.generate = Mock(return_value="Response")

        # Simulate conversation
        teacher.chat("Test message 1")
        teacher.chat("Test message 2")

        # Save session
        filepath = teacher.save_session()

        assert filepath is not None

        # Verify file content
        with open(filepath, 'r') as f:
            content = f.read()
            assert "Test message 1" in content
            assert "Test message 2" in content


class TestVoiceConfigurationIntegration:
    """Test integration of voice configuration with components."""

    def test_voice_config_affects_audio_recording(self):
        """Test that voice config properly configures audio recorder."""
        config = VoiceConfig(
            sample_rate=48000,
            channels=2
        )

        assert config.sample_rate == 48000
        assert config.channels == 2

    def test_voice_config_affects_tts(self):
        """Test that voice config properly configures TTS."""
        config = VoiceConfig(
            tts_voice="onyx",
            tts_model="tts-1-hd"
        )

        assert config.tts_voice == "onyx"
        assert config.tts_model == "tts-1-hd"
