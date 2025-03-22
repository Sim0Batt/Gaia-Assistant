from openai import OpenAI
import ollama

class AI:
    def __init__(self):
      self.client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
      )

    def generate_code(self, message):
      completion = self.client.chat.completions.create(
        model="deepseek/deepseek-r1-distill-llama-70b:free",
        messages=[
          {
            "role": "user",
            "content": f"{message}. GIVE ME ONLY THE CODE, NO EXPLANATION AND NO INTRODUCTION"
          }
        ]
        )
      return completion.choices[0].message.content

      

