from summarize_class import Summarizer

# Create a summarizer instance
summarizer = Summarizer()

# Test the model
test_phrases = [
    "Write a Python script.",
    "Show me the latest articles.",
    "Launch the calculator app.",
    "open firefox",
    "need to study",
    "power off the computer",
    "open my agenda",
    "read my todos",
]

summarizer._train_new_model()

for phrase in test_phrases:
    print(summarizer.predict(phrase))