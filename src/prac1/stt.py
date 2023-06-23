import speech_recognition as sr

rec = sr.Recognizer()
seconds = 3

with sr.Microphone() as source:

    print("Calibrating")
    rec.adjust_for_ambient_noise(source, duration=seconds)
    print("Set minimum energy threshold to " + str(rec.energy_threshold))

    print("Listening")
    audio = rec.listen(source, timeout=None, phrase_time_limit=None)
    print("End listening...")
    try:
        text = rec.recognize_google(audio)
        print(format(text))
    except:
        print("Error recognizing")
