import openai
import config
audio_file= open("output.wav", "rb")
openai.api_key = config.configDict["key"]
transcript = openai.Audio.translate("whisper-1", audio_file)
print(transcript)

