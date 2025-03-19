import os
import playsound
#import speech_recognition as sp
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
import datetime

from audio_set import setup as st
from dict import dictionary as dt
from minerva.todos.getTodos import FirestoreListener as fl
from minerva.notesReferences.notes import NoteLink as nl
from minerva.readCalendar.readCalendar import ReadCalendar as calendar
from apollo.AI import AI as ai
from efesto.summarize_class import Summarizer as sm




db = firestore.client()
def chooseAccount(decision):
    if decision == 1:
        accountDoc = "simonebatt51@gmail.com"
    elif decision == 2:
        accountDoc = "simone.battisti.fm@gmail.com"
    return accountDoc

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

def open_app(list_of_words):
    if 'firefox' in list_of_words:
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window"])
        return "apro Firefox"
    elif 'code' in list_of_words:
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "code"])
        return "apro Visual Studio Code"
    elif 'agenda' in list_of_words:
        open_todo()
        return "apro agenda"
    elif 'gpt' in list_of_words:
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://chatgpt.com/; exit"])
        return "apro ChatGPT"

    
def open_notes(list_of_words):
    subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://www.overleaf.com/project; exit"])
    subprocess.run(["gnome-terminal", "--", "bash", "-c", "emacs università/appuntiLatex/"])


def open_todo():
    accountDoc = ""
    decision = simpledialog.askstring("Input", "Inserisci account (1 - 2):") 
    while(int(decision) < 1 and int(decision) > 2):
        decision = simpledialog.askstring("Input", "Inserisci account (1 - 2):") 
    accountDoc = chooseAccount(int(decision))
    todo_ref = db.collection((accountDoc))
    todos = fl(accountDoc)
    time.sleep(0.75)
    content = todos.get_data_string()
    open_popup(content, 300, 400)
    return "letta agenda"

class Gaia():
    def __init__(self):
        self.summarizer = sm()
        self.ai_reference = ai()

    
    def get_response(self, text_in):
        predict = self.summarizer.predict(text_in)
        print(predict)
        list_of_words = text_in.split()
        if predict == "open":
            open_app(list_of_words)
        elif predict == "notes" or predict == "study":
            open_notes(list_of_words)
        elif predict == "read":
            open_todo()
            return "apro lettura"
        elif predict == "code":
            generated_code = self.ai_reference.generate_code(text_in)
            date = datetime.datetime.now()
            f = open(f"/home/simone/gaia/apollo/generated_code/generated-{str(date)[0:19]}.txt", "w")
            f.write(generated_code)
            f.close()
            return "generato codice"