# recorder.py
import speech_recognition as sr

def listen_and_convert(timeout=6, phrase_time_limit=8):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for background noise… please wait.")
        r.adjust_for_ambient_noise(source, duration=0.7)
        print("🎤 Talk now… (example: 'pizza 200, tea 50, sandwich 100')")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    try:
        text = r.recognize_google(audio)
        print("Recognized:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print("Speech service error:", e)
        return None
