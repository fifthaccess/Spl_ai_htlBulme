import openai
import pyttsx3 as tts
import speech_recognition as sr
import config 


openai.api_key = config.configDict["key"]
engine = tts.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[config.configDict["voice"]].id) # 10 für dietpi; 0 für test rechner

# Set up the OpenAI Playgroundhttps://beta.openai.com/playground/
openai.api_base = "https://api.openai.com/v1"

#TODO implementiere erkennung auf Athena/name 
prompt = "schrieb mir einen kurzen deutsch text auf deutsch"
while True:

    prompt = input()
    if not("?" in prompt):
        prompt = prompt + "?"

    print("prompt: '" + prompt + "'")

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=3500,
        n=1,
        stop=None,
        temperature=0.1,
    )


    print(response.choices[0].text)
    #TODO maybe logfiles schreiben 
    engine.say("chat GPT sagt:"+ response.choices[0].text )
    engine.runAndWait()