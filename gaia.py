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
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import tkinter as tk
from tkinter import simpledialog


from audio_set import setup as st
from dict import dictionary as dt
from summaryzeAI.predict import predict
from project_apollo.todos.getTodos import FirestoreListener as fl
from project_apollo.codeGeneratorCHATGPT.codeGenerator import codeGeneratorAPI as cg
from project_apollo.notesReferences.notes import NoteLink as nl
from project_apollo.readCalendar.readCalendar import ReadCalendar as calendar

key_words =["apri", "leggi", "ciao", "pulisci", "chiudi", "cerca", "wolfram", "codice", "spegni", "gpt"]



db = firestore.client()
def chooseAccount(decision):
    if decision == 1:
        accountDoc = "simonebatt51@gmail.com"
    elif decision == 2:
        accountDoc = "simone.battisti.fm@gmail.com"
    return accountDoc

def openApp(appName, text_in):
    if appName == "firefox":
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window"])

    elif appName == "cod":
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "code"])
        return "apro Visual Studio Code"

    elif appName in ["agenda", "todo"]:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        todo_path = os.path.join(current_dir, "project_apollo", "todos", "openTodo.py")
        subprocess.run(["gnome-terminal", "--", "bash", "-c", f"python3 {todo_path}"])
        return "apro agenda"

    elif appName == "appunti":
        controller = nl("")
        for item in controller.GetMaterie():
            if(item in text_in):
                controller = nl(item)
                OpenNotes(item, controller)
                return f"apro appunti {item}" 
        nome_materia = show_input_dialog()
        OpenNotes(nome_materia, controller)
    
    elif appName == "gpt":
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://chatgpt.com; exit"])


def OpenNotes(nomeMateria, controller):
    if(nomeMateria != ""):
        subprocess.run(["gnome-terminal", "--", "bash", "-c", f"firefox -new-window {controller.GetLink()}; exit"])
        if nomeMateria == "reti logiche":
            controller.openRetiLogiche()
        elif nomeMateria == "avanzata":
            controller.openProgAvanzata()
        else:
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://webapps.unitn.it/gestionecorsi/; exit"])
    else:
        nomeMateria = show_input_dialog()
        controller = nl(str(nomeMateria).strip())
        if(nomeMateria != ""):
            subprocess.run(["gnome-terminal", "--", "bash", "-c", f"firefox -new-window {controller.GetLink()}; exit"])
            if nomeMateria != "reti logiche":
                subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://webapps.unitn.it/gestionecorsi/; exit"])
            else:
               controller.openRetiLogiche()
        else:
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://www.overleaf.com/project; exit"])

def show_input_dialog():
    root = tk.Tk()
    root.withdraw()  
    input_text = simpledialog.askstring("Input Dialog", "Please enter your input:")

    if input_text is not None:
        print(f"Input received: {input_text}")
    else:
        print("No input received.")

    return input_text

def open_popup(content, width, height):
    todos_box = tk.Tk()
    todos_box.title("Another Root Window")
    todos_box.geometry(f"{width}x{height}")
        
    text_box = tk.Text(todos_box, wrap="word", width=50, height=10)
    text_box.pack(padx=10, pady=5, fill="both", expand=True)

    sample_text = content
    text_box.insert("1.0", sample_text)

    text_box.config(state="disabled")

    close_button = tk.Button(todos_box, text="Close", command=todos_box.destroy)
    close_button.pack(pady=5)

    todos_box.mainloop()


def generateCode(prompt):
    codeGenerator = cg(prompt)
    return codeGenerator.generate_code()


class Gaia():
    def GetResponse(text_in):
        text_in = str(text_in)
        if("'" in text_in):
            text_in = text_in.replace("'", " ")
        list_in = text_in.split()

        if len(list_in) > 0 and not text_in in key_words:
            w = predict.summarize_text(text_in)
            if ('"' in w):
                w = w.replace('"', '')
            w = w.strip()
        else:
            w = list_in[0]

        if w == "chiudi":
            exit()
            
        if w == "ciao":
            return("salve")

        if w == "leggi":
            for word in list_in:
                if word == "agenda":
                    accountMenuTxt ="""
    1) Personale (simonebatt51@gmail.com) \n
    2) Factory (simone.battisti.fm@gmail.com)
    """
                    accountDoc = ""
                    decision = simpledialog.askstring("Input", "Inserisci account (1 - 2):") 
                    while(int(decision) < 1 and int(decision) > 2):
                        decision = simpledialog.askstring("Input", "Inserisci account (1 - 2):") 
                    accountDoc = chooseAccount(int(decision))
                    print(accountDoc)
                    todo_ref = db.collection((accountDoc))
                    todos = fl(accountDoc)
                    time.sleep(0.75)
                    content = todos.get_data_string()
                    open_popup(content, 300, 400)
                    return "letta agenda"
                

                if word == "calendario":
                    if "studio" in text_in:
                        content = calendar.readStudioCalendar()
                        open_popup(str(content), 200, 100)
                        return str(content)
                    else:
                        open_popup("nessun calendario selezionato", 200, 100)


        if w == "apri":
            for word in list_in:
                openApp(word, text_in)

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

        if w == "codice":
            nomeFile = "test"
            pf = open(f"{nomeFile}.txt", "w")
            print(str(generateCode(text_in)))
        
        if w == "spegni":
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "poweroff"])
