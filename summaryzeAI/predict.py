from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the fine-tuned model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('./model')
tokenizer = T5Tokenizer.from_pretrained('./model')

class predict():
    def summarize_text(text):
        input_text = "summarize: " + text
        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate summary (this outputs token IDs, which we need to decode)
        summary_ids = model.generate(inputs['input_ids'], max_length=5, num_beams=2, early_stopping=True)
        
        # Decode the output to get the actual summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        return summary

    # if __name__ == "__main__":
    # input_text = "Artificial intelligence is intelligence demonstrated by machines."
    # print("Input:", input_text)
    # print("Summary:", summarize_text(input_text))


    
        