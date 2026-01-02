# core/stt.py
import numpy as np
import sounddevice as sd
import webrtcvad
from faster_whisper import WhisperModel

# STT model (English, optimized for speed)
WHISPER_MODEL = WhisperModel("tiny.en", device="cpu", compute_type="int8")

def transcribe_audio(audio: np.ndarray) -> str:
    """
    Transcribe 16kHz mono float32 audio (NumPy array) to text.
    """
    segments, _ = WHISPER_MODEL.transcribe(audio, beam_size=5, language="en")
    return " ".join(seg.text for seg in segments).strip()

# Voice Activity Detection
VAD = webrtcvad.Vad(2)  # Aggressiveness level: 0 (low) to 3 (high)

def is_speech(frame: np.ndarray, sample_rate: int = 16000) -> bool:
    """
    Check if a 10/20/30ms audio frame contains speech.
    Requires 16kHz sample rate and float32 input.
    """
    if sample_rate != 16000:
        raise ValueError("VAD requires 16kHz audio")
    # Convert float32 [-1.0, 1.0] to int16 PCM for webrtcvad
    frame_int16 = (frame * 32767).astype(np.int16)
    return VAD.is_speech(frame_int16.tobytes(), sample_rate)

def record_until_silence(
    timeout: float = 10.0,
    fs: int = 16000,
    silence_duration: float = 1.0
) -> np.ndarray:
    """
    Record audio from microphone until silence is detected.
    - Records up to `timeout` seconds (default: 10s)
    - Stops after `silence_duration` seconds of silence (default: 1s)
    - Returns audio as float32 NumPy array (mono, 16kHz)
    """
    chunk_duration = 0.03  # 30ms — valid for webrtcvad
    chunk_samples = int(chunk_duration * fs)
    silence_chunks = int(silence_duration / chunk_duration)
    timeout_chunks = int(timeout / chunk_duration)

    buffer = []
    silent_count = 0
    total_chunks = 0

    print("Listening... (speak now)")

    with sd.InputStream(samplerate=fs, channels=1, dtype='float32', blocksize=chunk_samples) as stream:
        while total_chunks < timeout_chunks:
            chunk, _ = stream.read(chunk_samples)
            chunk = chunk.squeeze()
            buffer.append(chunk)

            if is_speech(chunk, fs):
                silent_count = 0
            else:
                silent_count += 1

            # Stop if we've had enough silence and recorded something meaningful
            if silent_count >= silence_chunks and len(buffer) > int(0.5 / chunk_duration):
                print("Silence detected. Stopping recording.")
                break

            total_chunks += 1

    full_audio = np.concatenate(buffer) if buffer else np.array([], dtype=np.float32)
    duration = len(full_audio) / fs
    print(f"Recorded {duration:.1f} seconds of audio.")
    return full_audio