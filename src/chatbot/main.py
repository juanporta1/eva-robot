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
import pyaudio

class Eva:
    
    def __init__(self):
        self.is_recording = False
        self.finish = True
        self.is_new_talk = False
        self.audio = pyaudio.PyAudio()
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
            response,self.eva_context = chatbot_file.get_response(speech_to_text.convert(self.WAVE_OUTPUT_FILENAME),self.eva_context,name)
            text_to_speech.convert(response)
        
    def main(self):
        self.id = None
        print("Entrando en la funcion main")
        self.cap = cv2.VideoCapture(0)
        self.persons = db.getFaces()
        
        self.name = "Nadie"
        recognitionThread = threading.Thread(target=self.recognitionFunction)
        recognitionThread.start()
        while self.finish:
            self.record()
            self.get_response(self.name)
            if os.path.exists("src/chatbot/chatbot_audio.mp3") and self.is_new_talk:
                
                ps.playsound("src/chatbot/chatbot_audio.mp3",False)
                            
            
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print("Finalizaste la conversacion")
    
    def recognitionFunction(self):
        
        fps = 1.0 / 24
        while True:
            
            self.id  = None
            name = ""
            ret, self.frame = self.cap.read()
            
            self.encodeFace = []    
            if ret:
                frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                results = face_recognition.face_locations(self.frame)
                copyFrame = self.frame.copy()
                biggerArea = 0
                if results:
                    for detection in results:
                        top,right,bottom,left = detection
                        y = top
                        x = left
                        w = right - left
                        h = bottom - top
                        
                        self.encodeFace = face_recognition.face_encodings(self.frame,known_face_locations=[(y,x+w,y+h,x)])[0]             
                        cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0))
                        area = w * h
                        if area > biggerArea:
                            biggerArea = area
                            self.encodeFace = face_recognition.face_encodings(self.frame,known_face_locations=[(y,x+w,y+h,x)])[0]
            
                for person in self.persons:
                    if results:    
                        result = face_recognition.compare_faces([person[1]], self.encodeFace,.5)[0]
                        
                        if result == True:
                            name = person[0]
                            self.id = person[2]
                            break
                        else:
                            name = "Desconocido"
                            
        
                if not results:
                    name = "Nadie"
                
                self.securityEncode = self.encodeFace
            self.nameVar.set(self.name)
            cv2.imshow("Frame",self.frame)    
            if cv2.waitKey(1) == 27:
                break
            self.name = name
            print(self.id)
            time.sleep(fps)
        self.cap.release()
        cv2.destroyAllWindows() 
        
    def userController(self):
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
        