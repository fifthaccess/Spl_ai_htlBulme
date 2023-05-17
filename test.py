import openai
import pyttsx3 as tts
import speech_recognition
import config 


class AiBot: 
    def __init__(self):
        self._engine = tts.init()
        self._openAiKey = config.configDict["key"]

        voices = self._engine.getProperty('voices')
        self._engine.setProperty('voice',voices[config.configDict["voice"]].id) # 10 für dietpi; 0 für test rechner
        
        openai.api_key = self._openAiKey
        openai.api_base = "https://api.openai.com/v1"

    def gererateRespose(self, prompt):
        if not("?" in prompt):
            prompt = prompt + "?"
        prompt = " Beantworte auf Deutsch:" + prompt 
        print(prompt)
            
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=3500,
        n=1,
        stop=None,
        temperature=0.1,
        )
        self._termianl_answer(response= response)
        self._answer(response= response)

    def _answer(self, response):
        self._engine.say("chat GPT sagt:"+ response.choices[0].text)
        self._engine.runAndWait()    
    
    def _termianl_answer(self, response):
        print(response.choices[0].text)

myAI = AiBot()

while True:
    text = input()
    if ("Athena" in text):
        myAI.gererateRespose(text)
