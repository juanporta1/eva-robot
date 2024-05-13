import s as sr

# Crear un objeto Recognizer
recognizer = sr.Recognizer()

# Definir el dispositivo de entrada (micrófono)
mic = sr.Microphone()

# Configurar el reconocimiento de voz con el motor PocketSphinx
with mic as source:
    print("Escuchando...")
    # Calibrar el ruido de fondo para una mejor precisión (opcional)
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

# Convertir el audio en texto utilizando PocketSphinx
try:
    text = recognizer.recognize_sphinx(audio)
    print("Texto reconocido:", text)
except sr.UnknownValueError:
    print("No se pudo entender el audio")
except sr.RequestError as e:
    print("Error en la solicitud al servicio de reconocimiento de voz: {0}".format(e))