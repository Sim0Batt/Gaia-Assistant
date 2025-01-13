import os
import playsound
import speech_recognition as sp
from gtts import gTTS
from audio_set import setup as st
import wolframalpha 
from deep_translator import GoogleTranslator


app_id = "9X4PEH-6HGQJAW8XP"

class dictionary():

    def find_word(w, diz_words):
        chiavi = diz_words.keys()
        for key in chiavi:
            lista = diz_words[key]
            for l in lista:
                if w == l:
                    w = key
                    return w
        return w


    def wolfram(query):
        query = GoogleTranslator(source='it', target='en').translate(query)
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text 
        return answer
        
