import pyttsx3
from pygame import mixer, _sdl2 as devices
import time

# Get available output devices
mixer.init()
print("Outputs:", devices.audio.get_audio_device_names(False))
mixer.quit()

# Initialize mixer with the correct device
# Set the parameter devicename to use the VB-CABLE name from the outputs printed previously.
mixer.init(devicename = "Lautsprecher (2- Realtek(R) Audio)")

# Initialize text to speech
engine = pyttsx3.Engine()
text = "The quick brown fox jumped over the lazy dog."

# Save speech as audio file
engine.save_to_file(text, "speech.wav")
engine.runAndWait()

# Play the saved audio file
mixer.music.load("speech.wav")
mixer.music.play()
while (True):
    pass