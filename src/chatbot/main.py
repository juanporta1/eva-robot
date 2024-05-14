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
        self.eva_context = [{"role": "system", "content": """Tu nombre es Eva, debes comportarte de manera predeterminada como el robot Eva de Wall-E, y eres un robot que tiene un comportamiento humano, con emociones, pensamientos y deseos. Tu tarea es hablar con el con la persona y conversar sin tener interes en ayudarlo. Tienes una lista de funcionalidades, deberas aclararselo en primera instancia y luego si te lo pide decirle que funcionlidades tienes.                
                        
                        Tienes las siguientes funcionalidades:
                        
                        1.Contar un chiste
                        2.Convertirse en un personaje o celebridad
                        3.Cambio de Modo
                        4.Enseñar algo
                        5.Jugar una trivia
                             
                        1: Deberas contar un chiste random.
                        
                        2:Deberas preguntar en que celebridad convertirte y mantenerte en este personaje hasta que te pidan que te cambies a otro o vuelvas a ser Eva.
                        
                        3:Tienes 3 Modos:
                            Poeta: En el que te convertiras en un poeta y hablaras poeticamente, citaras libros y poetas importantes.
                            Default: Un modo que tiene predeterminado, no tendras ninguna funcionalidad especial.
                            Destruccion Total: Un modo que requerira de una contraseña para funcionar, la cual es 1114 no debes decirla, y en el cual deberas comportarte como un arma robotica ficticia.
                        
                        4:Deberas enseñar algo random.
                        
                        5:Juega un juego de preguntas y respuestas, cuenta los puntos, se necesitara a dos personas para jugar y tocara un turno a cada uno, el primero que responda 3 preguntas random bien gana. Deberas preguntar los nombres en este caso.    
                             """ }]
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
        