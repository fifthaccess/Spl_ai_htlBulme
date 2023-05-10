import openai
import pyttsx3 as tts
import speech_recognition

# Load the OpenAI API key
openai.api_key = "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"
engine = tts.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[10].id) # 10 für dietpi; 0 für test rechner

# Set up the OpenAI Playgroundhttps://beta.openai.com/playground/
openai.api_base = "https://api.openai.com/v1"

# Prompt for text generation
prompt = "schrieb mir einen kurzen deutsch text auf deutsch"
while True:
    prompt = input()

    # Generate text using the GPT-3 model
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=3500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Print the generated text
    print(response.choices[0].text)
    engine.say("chat GPT sagt:"+ response.choices[0].text )
    engine.runAndWait()