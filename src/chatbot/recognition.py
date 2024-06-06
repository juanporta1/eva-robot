import cv2
import face_recognition
import os
cap = cv2.VideoCapture(1)
count = 0

while cap.isOpened():

    ret, frame = cap.read()
    if ret == False: break
    frame = cv2.flip(frame,1)
    location = face_recognition.face_locations(frame)
    print(location)
    copyFrame = frame.copy()
    

    for top,right,bottom,left in location:
        cv2.rectangle(frame,(left,top),(right,bottom), (0,255,0),2) 

        encodeFace = face_recognition.face_encodings(frame,known_face_locations=[top,right,bottom,left])[0]
        result = face_recognition.compare_faces()
        
        rostro = cv2.resize(copyFrame[top:bottom,left:right],(150,150),interpolation=cv2.INTER_CUBIC)
        
        if count < 10:
            cv2.imwrite(os.getcwd() + "/src/chatbot/faces/{}.jpg".format(count),rostro)

    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) == 27:
        break
    count += 1
cap.release()
cv2.destroyAllWindows()