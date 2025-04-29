import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

class Summarizer:
    def __init__(self, model_path="/home/simone/gaia//knn_model.pkl", vectorizer_path="/home/simone/gaia/vectorizer.pkl", data_path="/home/simone/gaia/training_data.pkl"):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.data_path = data_path
        self.knn = None
        self.vectorizer = None
        self._load_or_train_model()

    def _load_or_train_model(self):
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path) and os.path.exists(self.data_path):
            self.knn = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            self.X_train, self.y_train = joblib.load(self.data_path)
        else:
            self._train_new_model()

    def _train_new_model(self):
        X_train = [
            # Open category
            "can you open this file?", "i need to launch an application.", "start the browser.",
            "open the document.", "launch the browser.", "start the editor.",
            "can you open chrome for me?", "open my music app.", "run the calculator.",
            "open the file in notepad.", "start the app.", "can you launch the terminal?",
            "open the settings panel.", "please open the webpage.", "launch vs code",
            "start spotify", "open system preferences", "launch the game",
            "start the media player", "open task manager",
            "hey, open this for me", "can ya start this app?", "fire up netflix",
            "lemme see that file", "just open it", "pull this up for me", "i need you to open this",
            "i want to see this", "open this up for me", "start this up",
            "open my app", "launch this program", "start my application",
            "open this software", "run this program", "start the program",
            "open that application", "launch my software", "get this running",
            "open the program for me", "start this software",

            # Notes_Making category
            "take some notes for me.", "save this information.", "write this down.",
            "take a note about the meeting.", "write down the to-do list.", "save this for later.",
            "can you note that down?", "take a quick note.", "write a reminder about my meeting.",
            "please jot this down.", "record this important detail.", "make a note about my appointment.",
            "save this idea for me.", "create a new note.", "write down my thoughts",
            "start a new note", "save this for reference", "take meeting minutes",
            "note the deadline", "write down the requirements", "add this to my notes",
            "create a memo", "document this", "keep a record of this",
            "save this note", "write this in my notebook",

            # Notes_Reading category
            "show me my notes.", "i need to read the notes", "check my previous notes.",
            "pull up the meeting notes.", "display my to-do list.", "view saved notes.",
            "can you show my notes?", "find my quick note.", "read my meeting reminders.",
            "show the saved details.", "access my recorded notes.", "view my appointment notes.",
            "find that note for me.", "open my recent notes.", "check my thought notes",
            "review meeting minutes", "show saved references", "look up my notes",
            "find the deadline note", "read the requirements", "display my memos",
            "find my documentation", "show my records", "access my saved notes",
            "open my notebook", "review my notes", "have to read my notes",

            # Read category
            "read the latest news.", "can you check this document?", "fetch data from the database.",
            "read the latest news.", "check the weather forecast.", "can you read my emails?",
            "please read this document.", "fetch the latest updates.", "read the book summary.",
            "show me the article.", "check for recent messages.", "can you read my messages?",
            "read the recent notifications.", "pull up the article on machine learning.", "read my schedule",
            "check the blog post", "read the documentation",
            "browse through papers", "check the latest posts",
            "give this a read", "what's this saying?", "check this out for me",
            "help me read through this", "what's new today?", "gimme the latest",

            # Code category
            "generate a python script.", "write a function for me.", "create some sample code.",
            "write a python function for addition.", "generate a code snippet for sorting.",
            "create a script that checks the file system.", "write a program to calculate the fibonacci sequence.",
            "can you code an api for data retrieval?", "write a javascript function for form validation.",
            "generate python code for web scraping.", "create a simple app in java.",
            "write a script to automate file backup.", "can you code a login page for me?",
            "write a program that finds prime numbers.", "code a simple game",
            "create a database query", "program a calculator", "develop a web app",
            "write an algorithm", "code a neural network",
            "help me code this", "gimme some code for this", "show me how to code",
            "need help with coding", "make this work in python", "fix this code",

            # Study category
            "i need to study", "time to study", "let's review the material",
            "i have to prepare for the exam", "need to revise", "study time",
            "have to learn this topic", "time for homework", "need to practice exercises",
            "let's do some studying", "have to review notes", "study session needed",
            "time to hit the books", "need to prepare", "have to study hard",
            "review time", "study break", "learning session",
            "time for revision", "need to concentrate",
            "gotta hit the books", "time to learn stuff", "help me study this",
            "need to cram", "let's get some studying done", "better start studying",

            # Switchoff category
            "shutdown the computer", "turn off the pc", "power down the system",
            "switch off my laptop", "can you shut down?", "time to power off",
            "please turn off the computer", "shutdown now", "power down",
            "turn off the machine", "system shutdown", "close everything and shutdown",
            "shut down the pc", "power off the laptop", "end all and shutdown",
            "time to turn off", "shutdown system", "power down now",
            "switch off system", "turn off everything",
            "kill the power", "shut it down", "turn this thing off",
            "power it down", "shutdown please", "need to turn off", "power off now", "time to go",

            # Close category
            "close yourself", "exit chatbot", "end conversation", 
            "terminate chat", "stop talking", "goodbye chatbot",
            "end this chat", "close the chat", "time to say goodbye",
            "finish conversation", "stop chatbot", "end this session",
            "close this conversation", "terminate session", "exit now",
            "bye chatbot", "end chat", "stop session",
            "close session", "time to go",
            "see ya later", "gotta go now", "let's end this",
            "time to quit", "wrap this up", "finish up now",
            "close this down", "end program", "stop program",
            "exit application", "quit chatbot", "time to finish",
            "end this program", "stop this chat", "close chat program",
            "quit program", "exit chat", "terminate program",
            "close application", "end application", "time to terminate",
        ]

        y_train = [
            # 41 open examples
            *["open"] * 41,
            # 26 make_notes examples
            *["make_notes"] * 26,
            # 27 read_notes examples
            *["read_notes"] * 27,
            # 25 read examples
            *["read"] * 25,
            # 25 code examples
            *["code"] * 25,
            # 26 study examples
            *["study"] * 26,
            # 27 switchoff examples
            *["switchoff"] * 27,
            # 42 close examples (adjusted to match X_train)
            *["close"] * 43
        ]

        self.vectorizer = TfidfVectorizer()
        X_train_vec = self.vectorizer.fit_transform(X_train)

        k = 3
        self.knn = KNeighborsClassifier(n_neighbors=k, metric='cosine')
        self.knn.fit(X_train_vec, y_train)

        joblib.dump(self.knn, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        joblib.dump((X_train, y_train), self.data_path)

    def predict(self, phrase):
        """Predict a summary word for the given phrase using k-NN."""
        X_new = self.vectorizer.transform([phrase])
        return self.knn.predict(X_new)[0]
