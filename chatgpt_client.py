from openai import OpenAI
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

question = input("Qual a sua pergunta para o ChatGPT? ")

def ask_question(question):
    response = client.chat.completions.create(
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
    return result

def create_mp3(result):
    language = 'en'
    mp3 = gTTS(text = f"{result}", lang=language)
    mp3.save(f'{question}.mp3')

answer = ask_question(question)
print(answer)
create_mp3(answer)
