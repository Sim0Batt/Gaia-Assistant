from todo import todo
import firebase_admin
from firebase_admin import firestore, credentials
import os
import time
import threading

# Check if the serviceAccount.json file exists
service_account_path = '/home/simone/gaia/minerva/todos/serviceAccount.json'  # Update path if needed
if not os.path.exists(service_account_path):
    raise FileNotFoundError("The serviceAccount.json file is missing. Please ensure it is in the correct directory.")

# Initialize Firebase
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Real-time snapshot callback
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        dictDocs = doc.to_dict()
        print(f"{dictDocs['id']} - {dictDocs['todo']}")

# Listen for updates
def printDB():
    listener = todo_ref.on_snapshot(on_snapshot)
    return listener  # Keep track of listener

# Account selection
def chooseAccount(decision):
    if decision == 1:
        return "simonebatt51@gmail.com"
    elif decision == 2:
        return "simone.battisti.fm@gmail.com"
    return None

def getDocs():
    return todo_ref.stream()  # Fetch fresh documents

# Clear terminal
def clearScreen():
    os.system("clear")

# Account selection menu
accountMenuTxt = """
1) Personale (simonebatt51@gmail.com) 
2) Factory (simone.battisti.fm@gmail.com)
"""
print(accountMenuTxt)
decision = int(input())
while decision not in [1, 2]:
    clearScreen()
    print(accountMenuTxt)
    decision = int(input())

accountDoc = chooseAccount(decision)
todo_ref = db.collection(accountDoc)

menuTxt = f"""
Account: {accountDoc}
1) Aggiungere TODO 
2) Stampa TODO 
3) Rimuovi 
4) Cambia Account 
5) Modifica Todo 
6) Esci
"""

# Keep track of listener
listener = printDB()

while True:
    print('.', end='', flush=True)
    print(menuTxt)
    printDB()
    

    decision = int(input())
    while decision not in range(1, 7):
        clearScreen()
        print(menuTxt)
        decision = int(input())
    clearScreen()

    if decision == 1:  # Add TODO
        lastId = max([int(doc.id) for doc in getDocs()] or [0]) + 1
        inputTask = input("Inserire todo: ")
        inputTodo = todo(lastId, inputTask)
        doc_ref = db.collection(accountDoc).document(f"{inputTodo.id}")
        doc_ref.set({"id": f"{inputTodo.id}", "todo": f"{inputTodo.task}"})

    elif decision == 2:  # Print TODOs
        printDB()
        time.sleep(0.75)

    elif decision == 3:  # Remove TODO
        printDB()
        time.sleep(0.75)
        indexRemove = input("Inserire ID: ")
        db.collection(accountDoc).document(indexRemove).delete()

    elif decision == 4:  # Change account
        print(accountMenuTxt)
        decision = int(input())
        accountDoc = chooseAccount(decision)
        todo_ref = db.collection(accountDoc)
        clearScreen()

        menuTxt = f"""
Account: {accountDoc} 
1) Aggiungere TODO 
2) Stampa TODO 
3) Rimuovi 
4) Cambia Account 
5) Modifica Todo 
6) Esci
"""
        listener = printDB()  # Restart listener

    elif decision == 5:  # Edit TODO
        clearScreen()
        printDB()
        time.sleep(0.75)
        print("Inserire ID del todo da modificare")
        docId = input()
        print("Inserire testo TODO")
        docTxt = input()
        db.collection(accountDoc).document(docId).update({"todo": docTxt})
        printDB()
        time.sleep(0.75)

    elif decision == 6:  # Exit
        exit()

    time.sleep(1)
