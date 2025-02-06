from openai import OpenAI

class AI:
    def __init__(self):
        self.client = OpenAI(
          base_url="https://openrouter.ai/api/v1",
          api_key="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",
        )

    def GetGenericResponse(self, message):
        completion = self.client.chat.completions.create(
          model="openai/gpt-3.5-turbo",
          messages=[
            {
              "role": "user",
              "content": message
            }
          ]
        )
        return completion.choices[0].message.content
