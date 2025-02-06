from todo import todo
import firebase_admin
from firebase_admin import firestore, credentials
import time
import threading
from google.cloud.firestore_v1.base_query import FieldFilter
import os
import subprocess

# Check if the serviceAccount.json file exists
service_account_path = 'minerva/todos/serviceAccount.json'  # Update this path as needed
if not os.path.exists(service_account_path):
    raise FileNotFoundError("The serviceAccount.json file is missing. Please ensure it is in the correct directory.")

#definition db
cred = credentials.Certificate(service_account_path)  # Use the updated path
firebase_admin.initialize_app(cred)
db = firestore.client()
# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        dictDocs = doc.to_dict()
        print(f"{dictDocs['id']} - {dictDocs['todo']}")

def printDB():
    todo_ref.on_snapshot(on_snapshot)

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


print(accountMenuTxt)
decision = int(input())
while(decision < 1 and decision > 2):
    clearScreen()
    print(accountMenuTxt)
    decision = int(input())
accountDoc = chooseAccount(decision)

menuTxt = f"""
Account: {accountDoc}
1) Aggiungere TODO \n
2) Stampa TODO \n
3) Rimuovi \n
4) Cambia Account \n
5) Modifica Todo \n
6) Esci
"""


todo_ref = db.collection(accountDoc)
docs = todo_ref.stream()
# Create an Event for notifying main thread.
callback_done = threading.Event()



while True:
    print('.', end='', flush=True)
    print(menuTxt)

    decision = int(input())
    while(decision < 1 or decision > 6):
        clearScreen()
        print(menuTxt)
        decision = int(input())
    clearScreen()



    #general code
    if(decision == 1):
        lastId = 0
        for doc in docs:
            lastId = doc.id
        lastId = int(lastId) + 1 


        inputTask = input("Inserire todo: ")

        inputTodo = todo(lastId, inputTask)
        doc_ref = db.collection(accountDoc).document(f"{inputTodo.id}")
        doc_ref.set({"id": f"{inputTodo.id}", "todo": f"{inputTodo.task}"})

    elif(decision == 2):
        printDB()
        time.sleep(0.75)
    
    elif(decision == 3):
        printDB()
        time.sleep(0.75)
        indexRemove = input("Inserire ID: ")
        db.collection(accountDoc).document(indexRemove).delete()

    elif decision == 4:
        print(accountMenuTxt)
        decision = int(input())
        accountDoc = chooseAccount(decision)
        todo_ref = db.collection(accountDoc)
        docs = todo_ref.stream()
        clearScreen()
        menuTxt = f"""
Account: {accountDoc} \n
1) Aggiungere TODO \n
2) Stampa TODO \n
3) Rimuovi \n
4) Cambia Account \n
5) Modifica Todo \n
6) Esci
"""
    
    elif decision == 5:
        clearScreen()
        printDB()
        time.sleep(0.75)
        print("Inserire ID del todo da modificare")
        docId = input()
        print("Inserire testo TODO")
        docTxt = input()
        db.collection(accountDoc).document(docId).delete()
        inputTodo = todo(docId, docTxt)
        doc_ref = db.collection(accountDoc).document(f"{inputTodo.id}")
        doc_ref.set({"id": f"{inputTodo.id}", "todo": f"{inputTodo.task}"})
        printDB()
        time.sleep(0.75)

    elif(decision == 6):
        exit()
    time.sleep(1)

    
