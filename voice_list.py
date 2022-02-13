import pyttsx3
engine = pyttsx3.init()
count = 0
voices = engine.getProperty('voices')
for voice in voices:
    print(f"[{count}] Voice: {voice.name} Languages: {voice.languages}")
    count = count + 1
