from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split

# Load and clean the dataset
df = pd.read_csv('./dataset.csv', header=None, names=['text', 'summary'])
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Split the dataset into training and evaluation sets
train_df, eval_df = train_test_split(df, test_size=0.2)  # 80% train, 20% eval
train_dataset = Dataset.from_pandas(train_df)
eval_dataset = Dataset.from_pandas(eval_df)

# Load a pre-trained T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small', legacy=False)   

# Tokenization: Prepare inputs for the model
def preprocess_data(example):
    input_texts = ["summarize: " + text for text in example['text']]
    target_texts = [summary for summary in example['summary']]
    
    inputs = tokenizer(input_texts, max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(target_texts, max_length=5, truncation=True, padding="max_length")
    
    inputs['labels'] = labels['input_ids']
    return inputs

# Apply preprocessing to both train and eval datasets
tokenized_train_dataset = train_dataset.map(preprocess_data, batched=True)
tokenized_eval_dataset = eval_dataset.map(preprocess_data, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',           # Output directory for checkpoints
    eval_strategy="epoch",      # Evaluation at the end of each epoch
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,     # Add this to batch your evaluation data as well
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    save_strategy="epoch"  # Save model at the end of every epoch
)

# Trainer initialization
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_eval_dataset
)

# Fine-tune the model
trainer.train()

# Save the trained model and tokenizer
model.save_pretrained('./model')
tokenizer.save_pretrained('./model')
