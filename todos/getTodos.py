import firebase_admin
from firebase_admin import firestore, credentials
import time
import threading
from google.cloud.firestore_v1.base_query import FieldFilter
import os
import subprocess


#Definition db
cred = credentials.Certificate('todos/serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def chooseAccount(decision):
    if decision == 1:
        accountDoc = "simonebatt51@gmail.com"
    elif decision == 2:
        accountDoc = "simone.battisti.fm@gmail.com"
    return accountDoc

def clearScreen():
    os.system("clear")

accountMenuTxt ="""
1) Personale (simonebatt51@gmail.com) \n
2) Factory (simone.battisti.fm@gmail.com)
"""
accountDoc = ""



todo_ref = db.collection(accountDoc)
docs = todo_ref.stream()
callback_done = threading.Event()


class FirestoreListener:
    def __init__(self, account_doc):
        self.account_doc = account_doc
        self.todo_ref = db.collection(self.account_doc)
        self.data_string = ""
        self.menu_txt = f"""
Account: {self.account_doc}
1) Aggiungere TODO \n
2) Stampa TODO \n
3) Rimuovi \n
4) Cambia Account \n
5) Modifica Todo \n
6) Esci
"""
        self._setup_listener()

    def _setup_listener(self):
        def on_snapshot(doc_snapshot, changes, read_time):
            data_list = []
            for doc in doc_snapshot:
                doc_data = doc.to_dict()
                data_list.append(f"{doc_data['id']} - {doc_data['todo']}")
            self.data_string = "\n".join(data_list)

        self.todo_ref.on_snapshot(on_snapshot)

    def get_data_string(self):
        return self.data_string

    @staticmethod
    def run_todos():
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "python3 openTodo.py"])
