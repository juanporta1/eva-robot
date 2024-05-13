import pyaudio
import wave

# Configurar los parámetros de grabación

import tkinter

class Eva:
    
    def __init__(self):
        self.is_recording = False
        root = tkinter.Tk()
        self.button = tkinter.Button(root,text="Presiona para hablar",command=self.talk)
        self.button.pack()
        
        self.eva_context = [{"role": "system", "content": "eres Eva,robot basado en la pelicula de wall-e. Recibiras un numero del 1 al 10 que es una escala de Agresividad/Amabilidad. Agresividad = 1, Amabilidad = 10. Si el mensaje se encuentra mas cerca del 1 deberas ser agresiva insultando tambien al usuario, si se encuentra mas cerca del 10 deberas ser amable." }]
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 10
        self.WAVE_OUTPUT_FILENAME = ""
        root.mainloop()
    
    def talk(self):
        if self.is_recording:
            self.is_recording = False
        else:
            self.is_recording = True
        
        
Eva()
        