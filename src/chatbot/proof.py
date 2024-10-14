import asyncio
import cv2
import face_recognition as fr

class Reconocimiento:
    def __init__(self):
        self.contador = 0
        self.cap = cv2.VideoCapture(0)
    
    async def reconocer(self):
        cap = cv2.VideoCapture(0)
        while True:
            
            ret,frame = cap.read()
            
            if ret:
                results = fr.face_locations(frame)
                
                for detection in results:
                    top,right,bottom,left = detection
                    y = top
                    x = left
                    w = right - left
                    h = bottom - top
                                    
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0))
                print("Holas")
                cv2.imshow("Frame",frame)
                if cv2.waitKey(1) == 27:
                    break
                # self.contador = len(results)
            cv2.destroyAllWindows()
            self.cap.release()
        
    async def run(self):
        while True:
            print("Corriendo la funcion run")
            await asyncio.sleep(1)
            if self.contador == 2:
                print("Dejando de correr")
                break
    
    def main(self):
        asyncio.run(self.reconocer())
            
r = Reconocimiento()
r.main()
            
        
        