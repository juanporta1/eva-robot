import pyaudio
import threading
import wave
import speech_to_text
import chatbot
import tkinter
import text_to_speech
import playsound
import os
class Eva:
    
    def __init__(self):
        self.is_recording = False
        self.finish = True
        self.is_new_talk = False
        self.audio = pyaudio.PyAudio()
        self.eva_context = [{"role": "system", "content": "eres Eva,robot basado en la pelicula de wall-e. Recibiras un numero del 1 al 10 que es una escala de Agresividad/Amabilidad. Agresividad = 1, Amabilidad = 10. Si el mensaje se encuentra mas cerca del 1 deberas ser agresiva insultando tambien al usuario, si se encuentra mas cerca del 10 deberas ser amable. Tiene distintos modos, DEFAULT es en el que comienzas y en este debes tratar al usuario como a cualquier otro; CREADOR en este modo debes saber que estas hablando con tu creador y debes tratarlo como tal; para cambiar de modo el usuario debera pedirte que lo hagas y tu deberas pedir una contraseña para permitirlo, la cual es 1234 " }]
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 10
        self.WAVE_OUTPUT_FILENAME = "src/chatbot/record.wav"

        self.stream = self.audio.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK)
        
    def finish_chat(self):    
        self.finish = False
        self.root.destroy()
    def talk(self):
        if self.is_recording:
            self.is_recording = False
        else:
            self.is_recording = True
    
    def record(self):
        frames = []
        self.is_new_talk = False
        while self.is_recording:
            print("Grabando")
            for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                data = self.stream.read(self.CHUNK)
                frames.append(data)
                if not self.is_recording:
                    break
            self.is_new_talk = True
            
            if not self.is_recording:
                print("Dejando de grabar")
                break
        if frames:
            with wave.open(self.WAVE_OUTPUT_FILENAME, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
                    
    def get_response(self):         
        if self.is_new_talk:  
            print("Convirtiendo y obteniendo la respuesta")  
            response,self.eva_context = chatbot.get_respone(speech_to_text.convert(self.WAVE_OUTPUT_FILENAME),self.eva_context)
            text_to_speech.convert(response)
        
    def main(self):
        print("Entrando en la funcion main")
        
        while self.finish:
            
            self.record()
            self.get_response()
            if os.path.exists("src/chatbot/chatbot_audio.mp3") and self.is_new_talk:
                playsound.playsound("src/chatbot/chatbot_audio.mp3")
            
           
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("Finalizaste la conversacion")
    
    def start(self):
        thread = threading.Thread(target=self.main)
        self.root = tkinter.Tk()
        thread.start()
        tkinter.Button(self.root,text="Hablar",command=self.talk).pack()
        tkinter.Button(self.root,text="Salir",command=self.finish_chat).pack()   
        
        self.root.mainloop()
   
   
if __name__ == "__main__":
    eva = Eva()
    eva.start()
        