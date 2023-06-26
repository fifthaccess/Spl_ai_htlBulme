import openai
import pyttsx3 as tts
import speech_recognition as sr
import config 
import paho.mqtt.client  as mqtt 
import socket
import sounddevice as sd
from scipy.io.wavfile import write
import logging

class AiBot: 
    def __init__(self):
        logging.basicConfig(filemode = 'a', filename='example.log',level=logging.INFO, encoding='utf-8', format='%(asctime)s %(message)s')
        hostname=socket.gethostname()   
        self.IPAddr=socket.gethostbyname(hostname)   

        self._engine = tts.init()
        
        self._openAiKey = config.configDict["key"]

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        #self.mqtt_client.connect(self.IPAddr, 1883, 60) 

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
        if ("licht" in prompt and ("ein" in prompt or "an" in prompt)) :
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
        
    def record(self,seconds = 3 ,sampleRate = 44100):
        print("listening")

        myrecording = sd.rec(int(seconds * sampleRate), samplerate=sampleRate, channels=2)
        sd.wait()  # Wait until recording is finished
        write('buffer.wav', sampleRate, myrecording)  # Save as mp3 file 

    def translate(self):

        audio_file= open("buffer.wav", "rb")
        openai.api_key = config.configDict["key"]
        transcript = openai.Audio.translate("whisper-1", audio_file)

        print(transcript["text"])

        input_text = openai.Completion.create(
                engine="text-davinci-002",
                prompt="Übersetzte nach deutsch:" + transcript["text"],
                max_tokens=3500,
                n=1,
                stop=None,
                temperature=0.1,
                )
        
        input_text = input_text.choices[0].text
        input_text = input_text.replace("\n","")

        print(input_text)
        if (not (input_text == "")): 
            logging.info('Received this: '+ input_text)
        return input_text
        
    def decide_answer(self,input_text):
            if ("led" in input_text.lower()):
               myAI.LED(input_text.lower())
            else:
                myAI.gererateRespose(input_text)


myAI = AiBot()

while True:
   
    myAI.record()   
    myAI.decide_answer(myAI.translate())