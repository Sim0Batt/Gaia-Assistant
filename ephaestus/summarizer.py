from summarize_class import Summarizer

# Create a summarizer instance
summarizer = Summarizer()

# Test the model
test_phrases = [
    "write a Python script.",
    "show me the latest articles.",
    "launch the calculator app.",
    "open firefox",
    "need to study",
    "power off the computer",
    "open the agenda",
    "read my todos",
    "i need to read my notes",
    "i want to make new notes"
]

summarizer._train_new_model()

for phrase in test_phrases:
    print(summarizer.predict(phrase))