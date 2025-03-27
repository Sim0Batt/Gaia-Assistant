import firebase_admin
from firebase_admin import firestore, credentials
import time
import threading
from google.cloud.firestore_v1.base_query import FieldFilter
import os
import subprocess
import time


#Definition db
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'serviceAccount.json'))
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
1) Aggiungere TODO
2) Stampa TODO
3) Rimuovi
4) Cambia Account
5) Modifica Todo
6) Esci
"""
        self._setup_listener()

    def _setup_listener(self):
        def on_snapshot(doc_snapshot, changes, read_time):
            try:
                data_list = []
                # Sort documents by ID before processing
                sorted_docs = sorted(doc_snapshot, key=lambda x: int(x.id))
                for doc in sorted_docs:
                    doc_data = doc.to_dict()
                    data_list.append(f"{doc_data['id']} - {doc_data['todo']}")
                self.data_string = "\n".join(data_list)
            except Exception as e:
                print(f"Error in snapshot handler: {e}")
                self.data_string = "Error loading todos"

        # Add a query constraint to listen to specific documents
        query = self.todo_ref.order_by('id')
        self.listener = query.on_snapshot(on_snapshot)

    def get_data_string(self):
        return self.data_string if self.data_string else "No todos found"

    @staticmethod
    def run_todos():
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "python /home/simone/gaia/minerva/todos/openTodo.py"])