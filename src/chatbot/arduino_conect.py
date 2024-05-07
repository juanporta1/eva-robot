import serial, time

def preguntar():
    arduino = serial.Serial("COM3",9600)
    time.sleep(1.5)

    datos=arduino.readline()
    print(datos.decode("utf-8"))
    return(datos.decode("utf-8"))

arduino = serial.Serial("COM3",9600)
time.sleep(1.5)
arduino.write(b"0")
time.sleep(1.5)
arduino.close()