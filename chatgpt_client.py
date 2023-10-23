import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")

question = input("Qual a sua pergunta para o ChatGPT? ")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a chatbot"},
        {"role": "user", "content": f"{question}"},
    ]
)

result = ''
for choice in response.choices:
    result += choice.message.content

print(f"Perguntamos ao chatGPT: {question}")
print(f"Aqui está a resposta dele: ")
print(result)