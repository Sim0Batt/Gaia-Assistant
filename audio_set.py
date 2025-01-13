import os
import playsound
import speech_recognition as sp
from random import randrange
from gtts import gTTS


class setup():
    def speak(text):
        tts =gTTS(text=text,lang='it')
        filename = "voce.mp3"
        if os.path.exists(filename):
            os.remove(filename)
        tts.save(filename)
        playsound.playsound(filename)

    def get_audio():
        r = sp.Recognizer()
        with sp.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=1)
            audio = r.listen(source)
            result = ""
            try:
                result = r.recognize_google(audio,language='it')
                print(result)
            except Exception as e:
                print("errore")
        return result
    