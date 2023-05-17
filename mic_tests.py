import speech_recognition as sr

with sr.Microphone() as source:
    print("listening: ")
    listner = sr.Recognizer()
    voice = listner.listen(source)
    command = listner.recognize_google(voice, language= 'de-at')
    print(command)