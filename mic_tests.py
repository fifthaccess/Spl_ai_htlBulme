import speech_recognition as sr
import pyaudio 




with sr.Microphone(device_index=2) as source:
    print("listening: ")
    listner = sr.Recognizer()
    voice = listner.listen(source)
    command = listner.recognize_google(voice, language= 'de-at')#, show_all=True
    print(command)


