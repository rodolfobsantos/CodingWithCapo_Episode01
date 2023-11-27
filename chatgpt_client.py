from openai import OpenAI
from gtts import gTTS
from dotenv import load_dotenv
import os
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


load_dotenv()

client = OpenAI()
webexToken = os.getenv("WEBEX_TOKEN")
webexRoomID = os.getenv("WEBEX_ROOMID")

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

def create_mp3(question, answer):
    # language = 'pt'
    # mp3 = gTTS(text = f"{answer}", lang=language, tld="com.br")
    language = 'en'
    mp3 = gTTS(text = f"{answer}", lang=language)
    mp3.save(f'{question}.mp3')

def send_chat_to_webex(question, answer):
    url = "https://webexapis.com/v1/messages"

    payload = json.dumps(
        { 
            "roomId": f"{webexRoomID}",
            "text": f"We asked chatGPT:\n{question}"
        }
    )

    headers = {
        "Authorization": f"Bearer {webexToken}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    print(f"The Webex API Call had a response code of {response}")

    # ChatGPT Answer
    payload = json.dumps(
        { 
            "roomId": f"{webexRoomID}",
            "text": f"Here was chatGPT's answer:\n{answer}"
        }
    )

    headers = {
        "Authorization": f"Bearer {webexToken}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    print(f"The Webex API Call had a response code of {response}")

def send_mp3_to_webex(question, answer):
    message_with_mp3 = MultipartEncoder(
        {
            "roomId": f"{webexRoomID}",
            "text": f"We asked chatGPT: {question}",
            "files": (f"{question}.mp3", open(f"{question}.mp3", 'rb'), 'audio/mp3')
        }
    )

    url = "https://webexapis.com/v1/messages"

    headers = {
        "Authorization": f"Bearer {webexToken}",
        "Content-Type": f"{message_with_mp3.content_type}"
    }

    response = requests.post(url, data=message_with_mp3, headers=headers)


pergunta = input("Qual a sua pergunta para o ChatGPT? ")

resposta = ask_question(pergunta)
print(resposta)
create_mp3(pergunta, resposta)

if webexToken:
    send_chat_to_webex(pergunta, resposta)
    send_mp3_to_webex(pergunta, resposta)