import cv2
import face_recognition

cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if ret == False: break
    frame = cv2.flip(frame,1)
    location = face_recognition.face_locations(frame)
    print(location)
    
    for face in location:
        cv2.rectangle(frame,(face[3],face[0]),(face[1],face[2]), (0,255,0),2)   
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()