# Librerías
from ultralytics import YOLO
import cv2

# Cargar el modelo
model = YOLO('best.pt')

# Nombre del archivo de video
video_filename = 'bus.mp4'  # Reemplaza esto con el nombre de tu archivo de video

# Videocaptura
cap = cv2.VideoCapture(video_filename)

# Verificar si el video se ha abierto correctamente
if not cap.isOpened():
    print("Error: No se puede abrir el archivo de video.")
    exit()

while True:
    # Captura de frame
    ret, frame = cap.read()

    # Si se ha llegado al final del video, salir del bucle
    if not ret:
        print("Fin del video")
        break

    # Realizar la predicción
    resultados = model.predict(frame, imgsz=640, conf=0.25)
    anotaciones = resultados[0].plot()

    # Mostrar los fotogramas
    cv2.imshow('DETECCION Y SEGMENTACION', anotaciones)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
