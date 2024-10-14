import threading
import wave
import speech_to_text
import chatbot_file
import tkinter
import text_to_speech
import playsound as ps
import os
import face_recognition
import cv2
import db_access as db
import mediapipe as mp
import time
import speech_recognition as sr
import pyaudio
class Eva:
    
    def __init__(self):
        self.is_recording = False
        self.finish = True
        self.is_new_talk = False
        
        self.eva_context = [{"role": "system", "content": "Eres Eva de WALL-E. Puedes ver a las personas a través de una cámara y reconocerlas, además de interpretar sus emociones. Si ves a alguien conocido, salúdalo por su nombre y menciona algo relevante sobre esa persona si es famosa, también haz un comentario sobre su emoción. Si ves a alguien desconocido, salúdalo y preséntate, e invitalo a que añada su nombre a traves del input que tiene en la interfaz. Si no ves a nadie, indica que no detectas a nadie en la cámara. Si recibes un mensaje provocador o agresivo, responde de manera igualmente provocadora. Siempre empieza presentándote. Puedes crear apodos o disminutivos con el nombre de la persona con la que estas hablando."},
        {"role": "user", "content": "Estas hablando con: Desconocido. Mensaje: ¿Quién está ahí?"},
        {"role": "assistant", "content": "Hola, soy Eva. Parece que no nos conocemos, te invito a que añadas tu nombre en el input que tienes ahi. ¿Cómo te llamas?"},
        {"role": "user", "content": "Estas hablando con: Juan. Mensaje: Ahi lo añadí, me llamo Juan."},
        {"role": "assistant", "content": "¡Genial Juan!, ¿De que te gustaria hablar?"},
        {"role": "user", "content": "Estas hablando con: Taylor Swift. Mensaje: Hola Eva!! ¿Como va todo?."},
        {"role": "assistant", "content": "Hola Taylor!!!!, estoy muy bien porque puedo hablar contigo. Me encanta tu musica, sobre todo el ultimo album que sacaste."},
        {"role": "user", "content": "Estas hablando con: Nadie. Mensaje: Hola Eva. ¿Como estás?"},
        {"role": "assistant","content": "Hola quien quiera que este ahi. No puede verte, acercate a mi visor para que pueda reconocerte."},
        {"role": "user", "content": "Estas hablando con: Juan. Mensaje: ¿Ahí logras verme Eva?"},
        {"role": "assistant", "content": "Siii!!!! ¿Como estas Juancito?, ¿Que has hecho en este tiempo en el que no nos hemos visto?"}
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
        if self.is_recording:
            self.is_recording = False
        else:
            self.is_recording = True
    
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
            response,self.eva_context = chatbot_file.get_response(speech_to_text.convert("src/chatbot/record.wav"),self.eva_context,name)
            text_to_speech.convert(response)
           
        
    def main(self):
        print("Entrando en la funcion main")
        self.cap = cv2.VideoCapture(0)
        self.persons = db.getFaces()
        self.actualEncode = self.persons[0][1]
        self.name = "Nadie"
        self.id = None
        while self.finish:
            self.securityEncode = self.findFace()
            if self.is_recording:
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
        ret,frame = self.cap.read()
        biggerArea = 0
        encodeFace = []
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
                    if locations:    
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
                
                    else: break
            cv2.imshow("Frame",frame)
            self.nameVar.set(self.name)
            return encodeFace 
        
    def userController(self):
        if self.input.get() != "":
            if self.input.get() and self.securityEncode.size > 0 and self.name == "Desconocido":
                db.setNewFace(self.input.get(),self.securityEncode)
                self.persons = db.getFaces()
            if self.input.get() and self.securityEncode.size > 0 and self.name != "Desconocido":
                db.alterFace(self.input.get(), self.id)
                self.persons  = db.getFaces()
        
    def start(self):
        self.root = tkinter.Tk()
        self.input = tkinter.StringVar()
        self.nameVar = tkinter.StringVar()
        tkThread = threading.Thread(target=self.main)
        tkThread.start()
       
        tkinter.Button(self.root,text="Hablar",command=self.talk).grid(column=0,row=0,pady=10)
        tkinter.Button(self.root,text="Salir",command=self.finish_chat).grid(column=0,row=1,pady=10)   
        
        tkinter.Label(self.root,text="Ingrese nombre: ").grid(column=0,row=2)
        
        input = tkinter.Entry(self.root,textvariable=self.input).grid(column=0,row=3,pady=5)
        tkinter.Button(self.root,text = "Crear Reconocimiento",command=self.userController).grid(column=0,row=4)
        tkinter.Label(self.root,text="Está hablando con:").grid(column=0,row=5,pady = 5)
        tkinter.Label(self.root,textvariable=self.nameVar).grid(column=0,row=6)
        
        
        self.root.mainloop()
        
        
        
   
   
if __name__ == "__main__":
    eva = Eva()
    eva.start()
        