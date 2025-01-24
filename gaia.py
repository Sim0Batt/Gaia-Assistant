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
    try:
        if appName == "firefox":
            try:
                subprocess.run(["firefox", "-new-window"],)
            except:
                subprocess.run(["gnome-terminal", "--", "firefox", "-new-window"],)
            return "apro firefox"

        elif appName == "cod":
            try:
                # Remove the --display flag for VS Code
                subprocess.run(["code"],)
            except:
                subprocess.run(["gnome-terminal", "--", "code"],)
            return "apro Visual Studio Code"

        elif appName == "agenda" or appName == "todo":
            current_dir = os.path.dirname(os.path.abspath(__file__))
            todo_path = os.path.join(current_dir, "todos", "openTodo.py")
            subprocess.run(["python3", todo_path],)
            return "apro agenda"

        elif appName == "windsurf":
            try:
                # Remove the --display flag for Cursor
                subprocess.run(["windsurf"],)
            except:
                subprocess.run(["gnome-terminal", "--", "windsurf"],)
            return "apro windsurf"
        elif appName == "appunti":
            nome_materia = show_input_dialog()
            OpenNotes(nome_materia)
            
                
    except subprocess.CalledProcessError as e:
        print(f"Failed to open {appName}. Error: {e}")
        return f"Failed to open {appName}"


def OpenNotes(nomeMateria):
    controller = nl(nomeMateria)
    print(nomeMateria)
    if(nomeMateria != ""):
        subprocess.run(["gnome-terminal", "--", "bash", "-c", f"firefox -new-window {controller.GetLink()}; exit"])
        if nomeMateria != "reti logiche":
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://webapps.unitn.it/gestionecorsi/; exit"])
        else:
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "vim /home/simone/appuntiLatex/RetiLogiche.txt"])
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://scenesnap.co/app/education/course/46f5bf86-02da-4357-8ba8-dca0ba9504d2; exit"])

    else:
        nomeMateria = show_input_dialog()
        controller = nl(str(nomeMateria).strip())
        if(nomeMateria != ""):
            subprocess.run(["gnome-terminal", "--", "bash", "-c", f"firefox -new-window {controller.GetLink()}; exit"])
            if nomeMateria != "reti logiche":
                subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://webapps.unitn.it/gestionecorsi/; exit"])
            else:
                subprocess.run(["gnome-terminal", "--", "bash", "-c", "vim /home/simone/appuntiLatex/RetiLogiche.txt"])
                subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://scenesnap.co/app/education/course/46f5bf86-02da-4357-8ba8-dca0ba9504d2; exit"])
        else:
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://www.overleaf.com/project; exit"])

def show_input_dialog():
    # Create a new Tkinter root window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Show the input dialog
    input_text = simpledialog.askstring("Input Dialog", "Please enter your input:")

    # Print the received input
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

    # MAIN
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
        
        if w == "gpt":
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://chatgpt.com; exit"])
        
        if w == "spegni":
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "poweroff"])
