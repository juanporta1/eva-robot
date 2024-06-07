import cv2
import face_recognition
import os
from sshtunnel import SSHTunnelForwarder
import db_access as db
cap = cv2.VideoCapture(0)
persons = db.getFaces()
print(persons)
while True:
    result = False
    name = ""
    ret, frame = cap.read()     
    if ret:
        frame = cv2.flip(frame,1)
        locations = face_recognition.face_locations(frame)
        copyFrame = frame.copy()
        biggerFace = None
        biggerArea = 0
        
        for faceLocation in locations:
            top,right,bottom,left = faceLocation
            
            widht = right - left
            height = bottom - top
            area = widht * height
            encodeFace = face_recognition.face_encodings(frame,known_face_locations=[faceLocation])[0]
            if area > biggerArea:
                biggerFace = encodeFace  
                
            rostro = cv2.resize(copyFrame[top-10:bottom+10,left-10:right+10],(150,150),interpolation=cv2.INTER_CUBIC)
            
            cv2.rectangle(frame,(left,top),(right,bottom), (0,255,0),2)
        for person in persons:
            if locations:    
                image = cv2.imread(os.getcwd() + f"/src/chatbot/faces/{person[0]}.jpg")
                imageLoc = face_recognition.face_locations(image)[0]
                dbPerson = face_recognition.face_encodings(image,known_face_locations=[imageLoc])[0]
                result = face_recognition.compare_faces([dbPerson], encodeFace)[0]
                
                if result == True:
                    name = person[0]
                    print("Resultado: ",result, " Name: ", name)
                    break
                else:
                    name = "Desconocido"
            
                
                
        if not locations:
            name = "Nadie"
        cv2.imshow("Frame",frame)  
        
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows() 

                
            
        
        
        

 
