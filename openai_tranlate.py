import openai
import config

audio_file= open("output.wav", "rb")
openai.api_key = config.configDict["key"]
transcript = openai.Audio.translate("whisper-1", audio_file)
print(transcript["text"])

response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Übersetzte auf deutsch:" + transcript["text"],
        max_tokens=3500,
        n=1,
        stop=None,
        temperature=0.1,
        )

print(response.choices[0].text)