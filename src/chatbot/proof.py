import cv2
import face_recognition

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if ret == False: break
   
    
    cv2.imshow("Frame", frame)
    
    
   
cap.release()
cv2.destroyAllWindows()