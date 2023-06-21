import speech_recognition as sr
import pyaudio 
import config 



with sr.Microphone(device_index=config.configDict["device"]) as source:
    print("listening: ")
    listner = sr.Recognizer()
    voice = listner.listen(source)
    command = listner.recognize_google(voice, language= 'de-at')#, show_all=True
    print(command)


