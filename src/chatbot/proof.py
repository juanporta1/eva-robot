import cv2
import mediapipe as mp

# Inicializar MediaPipe Face Detection.
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Inicializar la detección de caras.
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# Capturar video desde la cámara.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la imagen a RGB.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Realizar la detección de caras.
    results = face_detection.process(frame_rgb)

    # Dibujar los cuadrados alrededor de las caras detectadas.
    if results.detections:
        for detection in results.detections:
            # Obtener la posición de la cara.
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            (x, y, w, h) = (int(bboxC.xmin * iw), int(bboxC.ymin * ih),
                            int(bboxC.width * iw), int(bboxC.height * ih))

            # Dibujar un rectángulo alrededor de la cara.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostrar el frame con las detecciones.
    cv2.imshow('MediaPipe Face Detection', frame)

    # Salir del bucle al presionar la tecla 'q'.
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Liberar los recursos.
cap.release()
cv2.destroyAllWindows()
