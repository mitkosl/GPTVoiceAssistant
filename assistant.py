import os
import openai
import pyttsx3
import speech_recognition as sr

api_key = os.environ.get('OPEN_AI_API_KEY')
openai.api_key = api_key
print(api_key)

#init text-to-speech engine
enigne = pyttsx3.init()
voices = enigne.getProperty('voices')
enigne.setProperty('voices', voices[0].id)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = ""
user_name = "mitkosl"
bot_name = "Jarvis"

while True:
    with mic as source:
        print("\n Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("Finished listening!")

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    prompt = user_name + ":" + user_input + "\n" + bot_name + ":"
    conversation += prompt

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=conversation,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_prnalty=0,
        temperature=0.5,
    )

    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(user_name + ":", 1)[0].split(bot_name + ":", 1)[0]

    conversation += response_str + "\n"
    print(response_str)

    enigne.say(response_str)
    enigne.runAndWait()