import cv2
import face_recognition

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame,1)

    cv2.imshow("Frame",frame)
    k = cv2.waitKey(1)

    if k == 27 & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()