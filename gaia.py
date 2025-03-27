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

from minerva.todos.getTodos import FirestoreListener as fl
from minerva.readCalendar.readCalendar import ReadCalendar as calendar
from apollo.AI import AI as ai
from ephaestus.summarize_class import Summarizer as sm






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
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window; exit"])

        return "opened Firefox"
    elif 'code' in list_of_words:
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "code"])
        return "opened Visual Studio Code"
    elif 'agenda' in list_of_words:
        open_todo()
        return "opened agenda"
    elif 'gpt' in list_of_words:
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://chatgpt.com/; exit"])
        return "opened ChatGPT"

    
def open_notes():
    subprocess.run(["gnome-terminal", "--", "bash", "-c", "firefox -new-window https://www.overleaf.com/project -new-tab https://webapps.unitn.it/gestionecorsi/"])
    subprocess.run(["gnome-terminal", "--", "bash", "-c", "emacs /home/simone/università/appuntiLatex/"])


def read_todo():
    account_doc = ""
    decision = simpledialog.askstring("Input", "Inserisci account (1 - 2):") 
    while(int(decision) < 1 and int(decision) > 2):
        decision = simpledialog.askstring("Input", "Inserisci account (1 - 2):") 
    account_doc = chooseAccount(int(decision))
    todo_ref = db.collection((account_doc))
    todo_ref = fl(account_doc)
    time.sleep(0.75)
    content = todo_ref.get_data_string()
    open_popup(content, 300, 400)
    return "reded todo"

def open_todo():
    account_doc = "1"
    todo_ref = fl(account_doc)
    time.sleep(0.75)
    todo_ref.run_todos()
    

def init_request(request):
    return request.lower().replace("gaia", "").strip()

class Gaia():
    def __init__(self):
        self.summarizer = sm()
        self.ai_reference = ai()
    def get_response(self, text_in):
        requests = []
        if "and" in text_in:
            requests = text_in.split('and')
            for i in range(len(requests)):
                requests[i] = requests[i].strip()
        else:
            requests.insert(0, text_in)

        for request in requests:
            request = init_request(request)
            if request == 'close':
                exit()
            predict = self.summarizer.predict(request)
            print(predict)
            list_of_words = text_in.split()
            if not ('gaia' in list_of_words):
                return
            if predict == "open":
                open_app(list_of_words)
            elif predict == "notes" or predict == "study":
                open_notes()
            elif predict == "read":
                read_todo()
                return "opened todo"
            elif predict == "code":
                generated_code = self.ai_reference.generate_code(text_in)
                date = datetime.datetime.now()
                f = open(f"/home/simone/gaia/apollo/generated_code/generated-{str(date)[0:19]}.txt", "w")
                f.write(generated_code)
                f.close()
                return "generated code" 
            elif predict == "switchoff":
                subprocess.run(["shutdown", "now"])
                return "shutting down"