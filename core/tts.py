# core/tts.py
import pyttsx3

class TTS:
    def speak(self, text: str):
        if not text.strip():
            return
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 200)
        engine.setProperty('volume', 0.9)
        engine.say(text)
        engine.runAndWait()