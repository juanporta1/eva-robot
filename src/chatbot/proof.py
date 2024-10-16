import cv2

# Inicializa la cámara (0 para la cámara por defecto)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

while True:
    # Captura frame por frame
    ret, frame = cap.read()

    # Verifica si la captura fue exitosa
    if not ret:
        print("No se pudo recibir frame (stream finalizado?)")
        break

    # Muestra el frame en una ventana
    cv2.imshow('Camara en Vivo', frame)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera el recurso de la cámara y cierra ventanas
cap.release()
cv2.destroyAllWindows()
