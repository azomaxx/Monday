# main.py
import signal
import sys
from core.stt import record_until_silence, transcribe_audio
from core.llm import chat_with_llm
from core.tts import TTS

# Initialize TTS once
tts = TTS()

def signal_handler(sig, frame):
    tts.speak("Fine. Leave. See if I care.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    tts.speak("Natasha Monday is awake. Say my name to activate.")
    print("Natasha is listening. Say 'Natasha' or 'Monday'... (Ctrl+C to quit)")
    print("-" * 60)
    
    while True:
        try:
            # Record voice (in-memory, up to 10s, stops after 1s silence)
            audio = record_until_silence()
            if len(audio) == 0:
                continue
                
            # Transcribe
            text = transcribe_audio(audio)
            if not text:
                tts.speak("Did not understand. Try again.")
                continue
                
            print(f"You said: '{text}'")
            
            # Wake word filtering
            lower_text = text.lower()
            if not (lower_text.startswith("natasha") or lower_text.startswith("monday")):
                print("Ignoring (no wake word).")
                continue
            
            # Strip wake word
            clean_text = lower_text
            if clean_text.startswith("natasha"):
                clean_text = clean_text[8:].strip()
            elif clean_text.startswith("monday"):
                clean_text = clean_text[6:].strip()
            if not clean_text:
                clean_text = text

            # Send to LLM
            print("Processing...")
            response = chat_with_llm(clean_text)
            print(f"Natasha: {response}")
            
            # Speak response
            tts.speak(response)
            print("-" * 60)
            
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            tts.speak("Ugh. My brain froze.")

if __name__ == "__main__":
    main()