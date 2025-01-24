from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import openai


# class codeGeneratorAPI():
#     def __init__(self, prompt):
#         self.model_name = "Salesforce/codegen-350M-multi"
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
#         self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
#         self.prompt = prompt



#     def generate_code(self):
#         inputs = self.tokenizer(self.prompt, return_tensors="pt")
#         outputs =self.model.generate(**inputs, max_length=2048)  # Adjust max_length as needed
#         code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return code

apiKey = "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"
class codeGeneratorAPI():
    def __init__(self, prompt):
        self.question = prompt
        self.apiKey = apiKey
        openai.api_key = self.apiKey
        
    

    def generate_code(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": self.question},
            ],
            max_tokens=4096, 
            temperature=0.7 
        )

        return response['choices'][0]['message']['content']

# prompt = "How does the ChatGPT API work?"
# response = generate_code(prompt)
# print(response)