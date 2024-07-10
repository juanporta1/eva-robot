import speech_recognition as sr
import wave as w
listener = sr.Recognizer()
with sr.Microphone() as source:
    cont = 0
    audios = []
    while cont != 5:
        audio = listener.listen(source,phrase_time_limit=10,timeout=None)
        print(cont)
        cont += 1
        audios.append(audio.get_wav_data())
        
    with w.open("proof.wav","wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        f.writeframes(b''.join(audios))
    
