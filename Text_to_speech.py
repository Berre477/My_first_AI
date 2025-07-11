from gtts import gTTS
import os

def text_to_speech(text,ln):
    try:
        tts = gTTS(text=text, lang=ln)
        tts.save("output.mp3")
        os.system("afplay output.mp3")


    except Exception as e:
        print(f"Error in text-to-speech: {e}")

