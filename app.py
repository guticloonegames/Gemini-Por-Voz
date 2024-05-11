import speech_recognition as sr
import google.generativeai as genai
from playsound import playsound
import subprocess
import os
import re

API_KEY = ''

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name='gemini-1.0-pro', safety_settings={
    'HARASSMENT': "BLOCK_NONE",
    'HATE': "BLOCK_NONE",
    'SEXUAL': "BLOCK_NONE",
    'DANGEROUS': "BLOCK_NONE"
})

m = sr.Recognizer()
chat = model.start_chat(history=[])

def capture_microphone():

    text = 'Nada foi dito'

    with sr.Microphone() as source:
        m.adjust_for_ambient_noise(source, duration=1)

        print('Say anything: ')
        audio = m.listen(source)
    try:
        print('Processando audio. Aguarde...')
        text = m.recognize_google(audio, language='pt-BR')
    except sr.UnknownValueError:
        print('Não entendi.')

    return text 


chat.send_message('Por favor me responda o mais resumidamente que você conseguir sendo seco e simples nas respostas')
chat.send_message('não use markdown')
while (1):
    if input('Quer continuar (y/n): ') == 'y': 
        text = re.sub(r"\*", "", chat.send_message(capture_microphone()).text)

        command = ['edge-tts', '--voice', 'pt-BR-AntonioNeural', '--text', text , '--write-media', 'output/a.mp3']
        subprocess.run(command)
        os.system('cls')
        
        print(text)
        playsound('output/a.mp3')
        os.remove('output/a.mp3')
    else: break



