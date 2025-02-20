from openai import OpenAI

class AI:
    def __init__(self):
      self.client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="YOUR-API-KEY",
      )

    def GetGenericResponse(self, message):
      completion = self.client.chat.completions.create(
        model="deepseek/deepseek-r1-distill-qwen-32b",
        messages=[
          {
            "role": "user",
            "content": f"rispondi a questa domanda in italiano: {message}"
          }
        ]
        )
      return completion.choices[0].message.content

    def generateSummary(self, text_in):
      completion = self.client.chat.completions.create(
        model="deepseek/deepseek-r1-distill-qwen-32b",
        messages=[
          {
            "role": "user",
            "content": f"Sei un chatbot che può aprire applicazioni, spegnere pc, leggere file, ecc. Ora ti darò una frase, tu riassumila in una di queste parole [apri, leggi, ciao, chiudi, ricerca, wolfram, codice, spegni, gpt, debug], se non trovi una parola tra queste adatte ritorna la parola nessuno, ritornami solo la parola, nient'altro. La frase è: {text_in}"
          }
       ]
      )
      return completion.choices[0].message.content