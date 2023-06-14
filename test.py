import openai
import pyttsx3 as tts
import speech_recognition as sr
import config 
import paho.mqtt.client  as mqtt 
import socket

class AiBot: 
    def __init__(self):
        hostname=socket.gethostname()   
        self.IPAddr=socket.gethostbyname(hostname)   

        self._engine = tts.init()
        
        self._openAiKey = config.configDict["key"]

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect

        self.mqtt_client.connect(self.IPAddr, 1883, 60) # 

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
        self._termianl_answer(response= response.choices[0].text)
        self._answer(response= response.choices[0].text)
        
    def LED(self, prompt):
        print(prompt)
        if ("licht" in prompt and "ein" in prompt) :
            self.mqtt_client.publish('LED', payload=1 , qos=0, retain=False)
            self._answer("LED ein")
            self._termianl_answer("LED ein")

        if ("licht" in prompt and "aus" in prompt):
            self.mqtt_client.publish('LED', payload=0 , qos=0, retain=False)
            self._answer("LED aus")
            self._termianl_answer("LED aus")


    def _answer(self, response):
        self._engine.say(""+ response)
        self._engine.runAndWait()    
    
    def on_connect(self,client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def _termianl_answer(self, response):
        print(response)

myAI = AiBot()

while True:
    
    with sr.Microphone(device_index=config.configDict["device"]) as source:
        print("listening: ")
        listner = sr.Recognizer()
        voice = listner.listen(source)
        try:
            text = listner.recognize_google(voice, language= 'de-at')#, show_all=True
        except speech_recognition.exceptions.UnknownValueError:
            pass

        #print(command)

        #text = input()
        if ("Athena" in text):
            if ("led" in text.lower()):
                myAI.LED(text.lower())
            else:
                myAI.gererateRespose(text)
        else:
            print(text)