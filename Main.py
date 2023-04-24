import speech_recognition
import json
import openai
import pyttsx3

openai.api_key = "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"
g =openai.Model.list()
sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.8
input_text = ''
message_history = []

with open('message_history.json', encoding ='utf-8') as outfile:
    message_history_stab = json.load(outfile)
def Mic():
    query = ''
    with speech_recognition.Microphone() as mic:
        sr.adjust_for_ambient_noise(source=mic, duration=1)
        print(1)
        try:
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
        except speech_recognition.exceptions.UnknownValueError:
            print('Простите я прослушал')
    return query
def chatgpt_conversation(content):
    mem = [i for i in message_history_stab] + [i for i in message_history[max(0,len(message_history)-16):]]
    mem.append({"role": "user","content": content})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = mem,
    )
    
    reply_content = response.choices[0].message.content
    
    return reply_content
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

while True:
    if input_text == '':
        input_text = Mic()
        if input_text == '':
            continue
        print(f'User - {input_text}')
    n = chatgpt_conversation(input_text)
    print(f'AI - {n}')
    if input('(y/n)') == 'y':
        message_history.append({"role": "user","content": input_text})
        message_history.append({"role": "assistant","content": n})
        input_text = ''

        speak(n)
        
        
    
