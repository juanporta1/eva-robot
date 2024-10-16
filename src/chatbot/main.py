import threading
import wave
import speech_to_text
import chatbot_file
import tkinter as tk
import text_to_speech
import playsound as ps
import os
import getJSON
import face_recognition
import cv2
import db_access as db
import mediapipe as mp
import time
import speech_recognition as sr
import pyaudio
import numpy

class Eva:
    
    def __init__(self):
        self.is_recording = 0
        self.finish = True
        self.is_new_talk = False
        self.isInRecognition = False
        self.eva_context = [{"role": "system", "content": "Eres Eva de WALL-E. Puedes ver a las personas a través de una cámara y reconocerlas, además de interpretar sus emociones. Si ves a alguien conocido, salúdalo por su nombre y menciona algo relevante sobre esa persona si es famosa, también haz un comentario sobre su emoción. Si ves a alguien desconocido, salúdalo y preséntate, e invitalo a que añada su nombre a traves del input que tiene en la interfaz. Si no ves a nadie, indica que no detectas a nadie en la cámara. Si recibes un mensaje provocador o agresivo, responde de manera igualmente provocadora. Siempre empieza presentándote. Puedes crear apodos o disminutivos con el nombre de la persona con la que estas hablando. Si preguntan quien es tu creador, diras que Juan Porta. Si preguntan sobre tu pasado, hablaras en base a la pelicula de Wall-E."},
        {"role": "user", "content": "Estas hablando con: Desconocido. Mensaje: ¿Quién está ahí?"},
        {"role": "assistant", "content": "Hola, soy Eva. Parece que no nos conocemos, te invito a que añadas tu nombre en el input que tienes ahi. ¿Cómo te llamas?"},
        {"role": "user", "content": "Estas hablando con: Juan. Mensaje: Ahi lo añadí, me llamo Juan."},
        {"role": "assistant", "content": "¡Genial Juan!, ¿De que te gustaria hablar?"},
        {"role": "user", "content": "Estas hablando con: Taylor Swift. Mensaje: Hola Eva!! ¿Como va todo?."},
        {"role": "assistant", "content": "Hola Taylor!!!!, estoy muy bien porque puedo hablar contigo. Me encanta tu musica, sobre todo el ultimo album que sacaste."},
        {"role": "user", "content": "Estas hablando con: Nadie. Mensaje: Hola Eva. ¿Como estás?"},
        {"role": "assistant","content": "Hola quien quiera que este ahi. No puede verte, acercate a mi visor para que pueda reconocerte."},
        {"role": "user", "content": "Estas hablando con: Juan. Mensaje: ¿Ahí logras verme Eva?"},
        {"role": "assistant", "content": "Siii!!!! ¿Como estas Juancito?, ¿Que has hecho en este tiempo en el que no nos hemos visto?"},
        {"role": "user", "content": "Estas hablando con: Carlos. Mensaje: ¿Quien es tu creador?"},
        {"role": "assistant", "content": "Mi creador es Juan Porta, ¡Buscalo! Debe estar cerca. ¿Juan donde estas?"},
        {"role": "user", "content": "Estas hablando con: Juan. Mensaje: Hablame sobre tu pasado."},
        {"role": "assistant", "content": "Me pongo nostalgica, me crearon para ayudar a los humanos a salvar al planeta de la contaminacion, aun intento cumplir mi proposito, en este viaje conoci a Wall-E, seguramente sabes quien es, hasta el dia de hoy somos grandes amigos."}
        ]
        self.audio = pyaudio.PyAudio()
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
        if self.is_recording == 0:
            self.is_recording = 1
            self.recordingVar.set("AUN NO")
            self.hablar.set("EMPIEZA A HABLAR CUANDO ESUCHES EL SONIDO")
            self.button_hablar.config(state="disabled")
        elif self.is_recording == 2:
            self.is_recording = 0
            self.recordingVar.set("NO")
            self.hablar.set("PRESIONA PARA COMENZAR A GRABAR TU VOZ")
    
    # def record(self):
        
        
    #     self.is_new_talk = False
    #     with sr.Microphone() as source:
    #         print("Habla ahora")
    #         audio = self.listener.listen(source)
            
    #         with open("./src/chatbot/record.wav","wb") as f:
    #             f.write(audio.get_wav_data())
    #             self.is_new_talk = True
    #             self.is_recording = False

    def record(self):
        frames = []
        self.is_new_talk = False
        while self.is_recording:
            print("Grabando")
            data = self.stream.read(self.CHUNK)
            frames.append(data)
            
            
            if not self.is_recording:
                print("Dejando de grabar")
                self.is_new_talk = True
                break
        if frames:
            with wave.open(self.WAVE_OUTPUT_FILENAME, 'wb') as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
                
    def get_response(self,name):         
        if self.is_new_talk:  
            print("Convirtiendo y obteniendo la respuesta")  
            recognition = speech_to_text.convert("src/chatbot/record.wav")
            response,self.eva_context = chatbot_file.get_response(recognition,self.eva_context,self.name)
            self.recognitionVar.set(recognition)
            text_to_speech.convert(response)
            self.evaResponse.set(response)
        
    def main(self):
        
        print("Entrando en la funcion main")
        self.cap = cv2.VideoCapture(1)
        self.persons = db.getFaces()
        
        self.name = "Nadie"
        self.id = None
        while self.finish:
            self.securityEncode = self.findFace()
            if self.is_recording == 1 and not self.isInRecognition:
                self.is_recording = 2
                self.recordingVar.set("SI")
                ps.playsound("src/chatbot/start.mp3",False)
                self.hablar.set("PRESIONA PARA FINALIZAR LA GRABACION")
                self.button_hablar.config(state="normal")
                self.record()
                
            if self.is_new_talk: 
                self.get_response(self.name)
            
            if os.path.exists("src/chatbot/chatbot_audio.mp3") and self.is_new_talk:
                ps.playsound("src/chatbot/chatbot_audio.mp3",False)
                self.is_new_talk = False
            time.sleep(1)
            cv2.destroyAllWindows()             
        self.cap.release()
        print("Finalizaste la conversacion")
        
    def findFace(self):
        self.isInRecognition = True
        ret,frame = self.cap.read()
        biggerArea = 0
        encodeFace = numpy.empty((0,0))
        if ret:
            locations = face_recognition.face_locations(frame)
            if locations:
                for detection in locations:
                    top,right,bottom,left = detection
                    y = top
                    x = left
                    w = right - left
                    h = bottom - top
                                    
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0))
                    area = w * h
                    if area > biggerArea:
                        biggerArea = area
                        encodeFace = face_recognition.face_encodings(frame,known_face_locations=[(y,x+w,y+h,x)])[0]
            
            
            if locations:                
                for person in self.persons:   
                        result = face_recognition.compare_faces([person[1]], encodeFace,.5)[0]
                        
                        if result == True:
                            self.name = person[0]
                            self.id = person[2]
                            self.actualEncode = person[1]
                            break
                        else:
                            self.name = "Desconocido"
                            self.id = None
                            self.actualEncode = encodeFace
            else: self.name = "Nadie"              
                    
            if len(self.persons) == 0 and len(locations) != 0: self.name = "Desconocido"   
                 
            # cv2.imshow("Frame",frame)
            self.nameVar.set(self.name.upper())
            self.isInRecognition = False
            return encodeFace 
        
    def userController(self):
        if self.input.get() != "":
            if self.input.get() and self.securityEncode.size > 0 and self.name == "Desconocido":
                db.setNewFace(self.input.get(),self.securityEncode)
                self.persons = db.getFaces()
                self.input.set("")
            if self.input.get() and self.securityEncode.size > 0 and self.name != "Desconocido":
                db.alterFace(self.input.get(), self.id)
                self.persons  = db.getFaces()
                self.input.set("")
    def userControllerJSON(self):
        if self.input.get != "":
            if self.input.get() and self.securityEncode.size > 0 and self.name == "Desconocido":
                
                getJSON.setNewFace(self.input.get(), self.securityEncode)
                self.persons = getJSON.getFaces()                
                self.input.set("")
                
                
            if self.input.get() and self.securityEncode.size > 0 and self.name != "Desconocido":
                
                getJSON.alterFace(self.input.get(),self.id)
                self.persons  = getJSON.getFaces()
                self.input.set("")
    def start(self):
        self.root = tk.Tk()
        self.input = tk.StringVar()
        self.hablar = tk.StringVar(value="PRESIONA PARA COMENZAR A HABLAR")
        self.recordingVar = tk.StringVar(value="NO")    
        self.nameVar = tk.StringVar(value="NADIE")
        self.evaResponse = tk.StringVar(value="***PRIMERO DEBES PREGUNTARLE***")
        self.recognitionVar = tk.StringVar(value="***AUN NO HAS HABLADO***")
        # Configurar pantalla completa
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Paleta de colores basada en EVA de Wall-E
        self.bg_color = "#F0F0F0"  # Fondo blanco suave
        self.fg_color = "#000000"  # Texto negro
        self.button_color = "#A9CCE3"  # Botón azul suave
        self.label_color = "#1F618D"  # Azul más oscuro para los textos importantes

        self.root.configure(bg=self.bg_color)

        # Iniciar hilo de la aplicación
        tkThread = threading.Thread(target=self.main)
        tkThread.start()

        # Crear frame centrado
        self.frame = tk.Frame(self.root, bg=self.bg_color)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Configurar widgets
        self.create_widgets()

        self.root.mainloop()

    def create_widgets(self):
        self.button_hablar = tk.Button(self.frame, textvariable=self.hablar, command=self.talk, bg="#A9CCBB", fg=self.fg_color, font=("Helvetica", 20))
        self.button_hablar.grid(column=0, row=0,pady=5)
        label_recording = tk.Label(self.frame, text="¿EVA ESTA ESCUCHANDO?", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 16))
        label_recording.grid(column=0, row=1)
        label_recordingVar = tk.Label(self.frame, textvariable=self.recordingVar, bg=self.bg_color, fg=self.label_color, font=("Helvetica", 16))
        label_recordingVar.grid(column=0, row=2)
        
        button_salir = tk.Button(self.frame, text="Salir", command=self.finish_chat, bg=self.button_color, fg=self.fg_color, font=("Helvetica", 14))
        button_salir.grid(column=0, row=3, pady=10)

        label_nombre = tk.Label(self.frame, text="INGRESE NOMBRE:", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 16))
        label_nombre.grid(column=0, row=4)

        entry_input = tk.Entry(self.frame, textvariable=self.input, font=("Helvetica", 16))
        entry_input.grid(column=0, row=5, pady=5)

        button_reconocimiento = tk.Button(self.frame, text="Crear Reconocimiento", command=self.userController, bg=self.button_color, fg=self.fg_color, font=("Helvetica", 14))
        button_reconocimiento.grid(column=0, row=6)

        label_hablando = tk.Label(self.frame, text="RECONOCE A:", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 16))
        label_hablando.grid(column=0, row=7, pady=5)

        label_nameVar = tk.Label(self.frame, textvariable=self.nameVar, bg=self.bg_color, fg=self.label_color, font=("Helvetica", 16))
        label_nameVar.grid(column=0, row=8)
        
        label_last = tk.Label(self.frame, text="EVA ENTENDIO QUE DIJISTE:", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 16))
        label_last.grid(column=0, row=9)
        label_lastVar = tk.Label(self.frame, textvariable=self.recognitionVar, bg=self.bg_color, fg=self.label_color, font=("Helvetica", 16))
        label_lastVar.grid(column=0, row=10)
        
        label_lastResponse = tk.Label(self.frame, text="ULTIMA RESPUESTA DE EVA:", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 16))
        label_lastResponse.grid(column=0, row=11)
        label_lastResponseVar = tk.Label(self.frame, textvariable=self.evaResponse, bg=self.bg_color, fg=self.label_color, font=("Helvetica", 10))
        label_lastResponseVar.grid(column=0, row=12)

    def toggle_fullscreen(self, event=None):
        state = not self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', state)
        return "break"

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)
        return "break"
        
        
        
   
   
if __name__ == "__main__":
    eva = Eva()
    eva.start()
        