import cv2
import face_recognition
# Imagen a comparar

'''
cv2.rectangle(image, (face_loc[3], face_loc[0]), (face_loc[1], face_loc[2]), (0, 255, 0))
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
######################################################################################
# Video Streaming
cap = cv2.VideoCapture(1)
print(cap)
while True:
     print("Hola")
     ret, frame = cap.read()
     if ret == False: break
     frame = cv2.flip(frame, 1)
     face_locations = face_recognition.face_locations(frame, model="cnn")
     if face_locations != []:
          for face_location in face_locations:
               #print("Result:", result)
               color = (0,255,0)
               cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1)
               cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2)
               cv2.putText(frame, "Juan", (face_location[3], face_location[2] + 20), 2, 0.7, (255, 255, 255), 1)
     cv2.imshow("Frame", frame)
     k = cv2.waitKey(1)
     if k == 27 & 0xFF:
          break
cap.release()
cv2.destroyAllWindows()