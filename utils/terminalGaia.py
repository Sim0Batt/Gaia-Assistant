import os
import playsound
import speech_recognition as sp
from gtts import gTTS
from deep_translator import GoogleTranslator
# import pywhatkit as pw
from tqdm import tqdm
import wolframalpha
from time import sleep
import firebase_admin
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1.base_query import FieldFilter
import openai
import subprocess
import time

from utils.audio_set import setup as st
from summaryzeAI.predict import predict
from todos.getTodos import FirestoreListener as fl
from codeGeneratorCHATGPT.codeGenerator import codeGeneratorAPI as cg
from notesReferences.notes import NoteLink as nl


key_words =["apri", "leggi", "ciao", "pulisci", "chiudi", "cerca", "wolfram", "codice", "spegni"]

db = firestore.client()

def pulisciSchermo():
    os.system("clear")

def chooseAccount(decision):
    if decision == 1:
        accountDoc = "simonebatt51@gmail.com"
    elif decision == 2:
        accountDoc = "simone.battisti.fm@gmail.com"
    return accountDoc

def openApp(appName, text_in):
    request = str(text_in)
    if appName == "firefox":
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window; exit"])
        st.speak("apro firefox")

    elif appName == "cod":
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "code"])
        st.speak("apro Visual Studio Code")

    elif appName == "agenda" or appName == "todo":
        subprocess.run(
            ["gnome-terminal", "--", "bash", "-c", f"python3 openTodo.py; exec bash"],
            cwd="todos"  # Set the working directory
        )
        st.speak("apro agenda")

    elif appName == "appunti":
        nomeMateria = ""
        controller = nl("")
        request = request.replace(appName, '').strip()
        request = request.replace('apri', '').strip()
        request = request.split()
        subjectsList = controller.GetMaterie()

        for sub in subjectsList:
            for w in request:
                if(w.strip() == str(sub).strip()):
                    nomeMateria = sub


        if(nomeMateria == None):
            nomeMateria = input("Materia? ")
        controller = nl(nomeMateria)
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://webapps.unitn.it/gestionecorsi/; exit"])
        if(nomeMateria == None):
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://www.overleaf.com/project; exit"])
        else:
            subprocess.run(["gnome-terminal", "--", "bash", "-c", f"firefox -new-window {controller.GetLink()}; exit"])





def generateCode(prompt):
    codeGenerator = cg(prompt)
    return codeGenerator.generate_code()



pulisciSchermo()
# print("AVVIO IN CORSO")
# for i in tqdm(range(100)):
#     sleep(0.001)
# pulisciSchermo()
# print("Avvio completato!")
# print("\a")
# sleep(0.75)
# pulisciSchermo()

# MAIN
while True:
    # if keyboard.is_pressed("space"):
    #     text_in = st.get_audio()
    text_in = input()  # per prove no audio
    text_in = text_in.lower()

    if("'" in text_in):
        text_in = text_in.replace("'", " ")
    list_in = text_in.split()

    if len(list_in) > 0 and not text_in in key_words:
        w = predict.summarize_text(text_in)
        if ('"' in w):
            w = w.replace('"', '')
        w = w.strip()
        print(w)
    else:
        w = list_in[0]

    if w == "chiudi":
        pulisciSchermo()
        exit()

    if w == "pulisci":
        pulisciSchermo()

    if w == "ciao":
        st.speak("salve")

    if w == "leggi":
        for word in list_in:
            if word == "agenda":
                accountMenuTxt ="""
1) Personale (simonebatt51@gmail.com) \n
2) Factory (simone.battisti.fm@gmail.com)
"""
                accountDoc = ""
                print(accountMenuTxt)
                decision = int(input())
                while(decision < 1 and decision > 2):
                    pulisciSchermo()
                    print(accountMenuTxt)
                    decision = int(input())
                accountDoc = chooseAccount(decision)

                todo_ref = db.collection(accountDoc)
                todos = fl(todo_ref)
                print(fl.get_data_string(todos))

    if w == "apri":
        for word in list_in:
            openApp(word, text_in)
            #elif word == "wolfram":
            #     st.speak("Ho aperto wolfram, cosa si vuole sapere?")
            # while True:
            #     try:
            #         # query = st.get_audio()
            #         query = input()
            #         query = query.lower()
            #         list_in = query.split(' ')
            #         if query == "chiudi":
            #                 pulisciSchermo()
            #                 break
            #         if query == "pulisci":
            #             pulisciSchermo()
            #             res = dt.wolfram(query)
            #             res = GoogleTranslator(
            #             source='en', target='it').translate(res)
            #             st.speak(res)
            #     except:
            #         st.speak("Non ho capito scusa")

    if w == "riproduci":
        if w in list_in:
            index = list_in.index(w)
            del list_in[0:index+1]
        if "youtube" in list_in:
            list_in.remove("youtube")
        txt = ' '.join(list_in)
        # pw.playonyt(txt)

    if w == "cerca":
        if "google" in list_in:
            list_in.remove("google")
        if "su" in list_in:
            list_in.remove("su")
        if w in list_in:
            index = list_in.index(w)
            del list_in[0:index+1]
        txt = ' '.join(list_in)
        # pw.search(txt)

    if w == "wolfram":
        if w in list_in:
            index = list_in.index(w)
            del list_in[0:index+1]
        st.speak("Ho aperto wolfram, cosa si vuole sapere?")
        while True:
            try:
                query = st.get_audio()
                # query = input()

                if query == "chiudi":
                    pulisciSchermo()
                    break
                if query == "pulisci":
                    pulisciSchermo()
                    res = dt.wolfram(query)
                res = GoogleTranslator(
                    source='it', target='en').translate(res)
                st.speak(res)
            except:
                st.speak("Non ho capito scusa")

    if w == "codice":
        nomeFile = "test"
        pf = open(f"{nomeFile}.txt", "w")
        print(str(generateCode(text_in)))
        # pf.close()
        
        # # Open the file in read mode and read all lines
        # with open(f"{nomeFile}.txt", "r") as file:
        #     lines = file.readlines()

        # # Remove the first line
        # lines = lines[1:]

        # # Open the file in write mode and write the remaining lines
        # with open(f"{nomeFile}.txt", "w") as file:
        #     file.writelines(lines)
        # print("finito")
    
    if w == "spegni":
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "poweroff"])


    else:
        continue
