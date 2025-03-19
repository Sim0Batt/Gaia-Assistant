from openai import OpenAI
import ollama

class AI:
    def __init__(self):
      self.client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="YOUR-API-KEY",
      )

    def generate_code(self, message):
      completion = self.client.chat.completions.create(
        model="deepseek/deepseek-r1-distill-llama-70b:free",
        messages=[
          {
            "role": "user",
            "content": f"Generate the code for {message}. GIVE ME ONLY THE CODE, NO EXPLANATION AND NO INTRODUCTION"
          }
        ]
        )
      return completion.choices[0].message.content

      

