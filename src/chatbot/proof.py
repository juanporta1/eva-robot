import speech_recognition as sr
import wave as w
listener = sr.Recognizer()


with sr.Microphone() as source:
    listener.adjust_for_ambient_noise(source)
    audio = listener.listen(source)
    
    with open("proof.wav", "wb") as f:
        f.write(audio.get_wav_data())
