"""Audio recording module for capturing microphone input."""

import pyaudio
import wave
import tempfile
import os
from typing import Optional


class AudioRecorder:
    """Records audio from the microphone."""

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        format: int = pyaudio.paInt16
    ):
        """Initialize the audio recorder.

        Args:
            sample_rate: Sample rate in Hz (16000 is optimal for Whisper)
            channels: Number of audio channels (1 for mono, 2 for stereo)
            chunk_size: Number of frames per buffer
            format: PyAudio format (paInt16 for 16-bit audio)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format = format
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        """Start recording audio from the microphone."""
        self.frames = []
        self.is_recording = True

        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        print("🎤 Recording... Press Enter when done speaking.")

    def stop_recording(self) -> str:
        """Stop recording and save to a temporary file.

        Returns:
            Path to the temporary audio file
        """
        self.is_recording = False

        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()

        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_path = temp_file.name
        temp_file.close()

        # Save recorded audio
        with wave.open(temp_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))

        print("✓ Recording saved")
        return temp_path

    def record_chunk(self):
        """Record a single chunk of audio."""
        if self.is_recording:
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            self.frames.append(data)

    def record_until_enter(self) -> str:
        """Record audio until user presses Enter.

        Returns:
            Path to the temporary audio file
        """
        import threading

        self.start_recording()

        # Record in background thread
        def record_loop():
            while self.is_recording:
                self.record_chunk()

        record_thread = threading.Thread(target=record_loop)
        record_thread.start()

        # Wait for Enter key
        input()

        # Stop recording
        temp_path = self.stop_recording()
        record_thread.join()

        return temp_path

    def cleanup(self):
        """Clean up audio resources."""
        if hasattr(self, 'stream') and self.stream.is_active():
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
