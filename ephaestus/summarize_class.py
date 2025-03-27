import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

class Summarizer:
    def __init__(self, model_path="knn_model.pkl", vectorizer_path="vectorizer.pkl", data_path="training_data.pkl"):
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
            "Can you open this file?", "I need to launch an application.", "Start the browser.",
            "Open the document.", "Launch the browser.", "Start the editor.",
            "Can you open Chrome for me?", "Open my music app.", "Run the calculator.",
            "Open the file in Notepad.", "Start the app.", "Can you launch the terminal?",
            "Open the settings panel.", "Please open the webpage.", "Launch VS Code",
            "Start Spotify", "Open system preferences", "Launch the game",
            "Start the media player", "Open task manager",
            "Hey, open this for me", "Can ya start this app?", "Fire up Netflix",
            "Lemme see that file", "Just open it", "Pull this up for me", "I need you to open this",
            "I want to see this", "Open this up for me", "Start this up",
            "Open my app", "Launch this program", "Start my application",
            "Open this software", "Run this program", "Start the program",
            "Open that application", "Launch my software", "Get this running",
            "Open the program for me", "Start this software",

            # Notes category
            "Take some notes for me.", "Save this information.", "Write this down.",
            "Take a note about the meeting.", "Write down the to-do list.", "Save this for later.",
            "Can you note that down?", "Take a quick note.", "Write a reminder about my meeting.",
            "Please jot this down.", "Record this important detail.", "Make a note about my appointment.",
            "Save this idea for me.", "Can you note this down for future reference?", "Note the phone number",
            "Write down the address", "Save this recipe", "Take meeting minutes",
            "Note the deadline", "Write down the requirements",
            "Jot this down real quick", "Just make a note of this", "Quick, write this down",
            "Remember this for me", "Gotta save this somewhere", "Keep this in your notes",

            # Read category
            "Read the latest news.", "Can you check this document?", "Fetch data from the database.",
            "Read the latest news.", "Check the weather forecast.", "Can you read my emails?",
            "Please read this document.", "Fetch the latest updates.", "Read the book summary.",
            "Show me the article.", "Check for recent messages.", "Can you read my messages?",
            "Read the recent notifications.", "Pull up the article on machine learning.", "Read my schedule",
            "Check the blog post", "Read the documentation",
            "Browse through papers", "Check the latest posts",
            "Give this a read", "What's this saying?", "Check this out for me",
            "Help me read through this", "What's new today?", "Gimme the latest",

            # Code category
            "Generate a Python script.", "Write a function for me.", "Create some sample code.",
            "Write a Python function for addition.", "Generate a code snippet for sorting.",
            "Create a script that checks the file system.", "Write a program to calculate the Fibonacci sequence.",
            "Can you code an API for data retrieval?", "Write a JavaScript function for form validation.",
            "Generate Python code for web scraping.", "Create a simple app in Java.",
            "Write a script to automate file backup.", "Can you code a login page for me?",
            "Write a program that finds prime numbers.", "Code a simple game",
            "Create a database query", "Program a calculator", "Develop a web app",
            "Write an algorithm", "Code a neural network",
            "Help me code this", "Gimme some code for this", "Show me how to code",
            "Need help with coding", "Make this work in Python", "Fix this code",

            # Study category
            "I need to study", "Time to study", "Let's review the material",
            "I have to prepare for the exam", "Need to revise", "Study time",
            "Have to learn this topic", "Time for homework", "Need to practice exercises",
            "Let's do some studying", "Have to review notes", "Study session needed",
            "Time to hit the books", "Need to prepare", "Have to study hard",
            "Review time", "Study break", "Learning session",
            "Time for revision", "Need to concentrate",
            "Gotta hit the books", "Time to learn stuff", "Help me study this",
            "Need to cram", "Let's get some studying done", "Better start studying"

            #Switchoff category
            "Shutdown the computer", "Turn off the PC", "Power down the system",
            "Switch off my laptop", "Can you shut down?", "Time to power off",
            "Please turn off the computer", "Shutdown now", "Power down",
            "Turn off the machine", "System shutdown", "Close everything and shutdown",
            "Shut down the PC", "Power off the laptop", "End all and shutdown",
            "Time to turn off", "Shutdown system", "Power down now",
            "Switch off system", "Turn off everything",
            "Kill the power", "Shut it down", "Turn this thing off",
            "Power it down", "Shutdown please", "Need to turn off", "Power off now"
        ]


        y_train = [
            # 26 open examples
            *["open"] * 41,
            # 26 notes examples
            *["notes"] * 26,
            # 26 read examples
            *["read"] * 25,
            # 26 code examples
            *["code"] * 26,
            # 26 study examples
            *["study"] * 26,
            # 26 switchoff examples
            *["switchoff"] * 26
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
