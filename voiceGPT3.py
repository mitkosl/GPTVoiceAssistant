import os
import time
import openai
import pyttsx3
import speech_recognition as sr

keyphrase = "genius"
filename = "userInput.wav"
#set open.AI API Key
api_key = os.environ.get('OPEN_AI_API_KEY')
openai.api_key = api_key
print(api_key)

#init text-to-speech engine
enigne = pyttsx3.init()


def transcribe_audio_to_text(file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Unknown error during recognizing audio")

def get_gpt_reponse(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5 
    )
    return response["choices"][0]["text"]

def speak(text):
    enigne.say(text)
    enigne.runAndWait()

def main():
    while True:
        # Wait for "keyphrase"
        print(f"Say: '{keyphrase}' to start recording your question...")
        speak(f"Say: '{keyphrase}' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")

            try:
                audio = recognizer.listen(source)
            except Exception as e:
                print("An error ocured while parsing: {}".format(e))

            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
            try:
                recognized_phrases = recognizer.recognize_google(audio, language = 'en-US', show_all=True)
                print(f"Recognized: {recognized_phrases}")
                phrases = [phrase.lower() for phrase in recognized_phrases]
                if(keyphrase in phrases):
                    # Record user question from audio
                    print("What is your question ?")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                        
                    # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        # Generate response using GPT3
                        response = get_gpt_reponse(text)
                        print(f"GPT-3 says: {response}")

                        # Read response out lout using text-to-speech
                        speak(response)
            except Exception as e:
                print("An error ocured while parsing: {}".format(e))


if __name__ ==  "__main__":
    main()