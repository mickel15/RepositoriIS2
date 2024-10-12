# Librerías
from ultralytics import YOLO
import cv2
# Cargar el modelo
model = YOLO('bestdetect.pt')

# Nombre del archivo de video de entrada y salida
video_filename = 'Bus.mp4'
output_filename = 'busConIAdetect.mp4'
# Videocaptura
cap = cv2.VideoCapture(video_filename)
# Verificar si el video se ha abierto correctamente
if not cap.isOpened():
    print("Error: No se puede abrir el archivo de video.")
    exit()
# Obtener el ancho, alto y fps del video original
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
# Definir el codec y crear el objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para el formato de video MP4
out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

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
    out.write(anotaciones)
    # Mostrar los fotogramas
    cv2.imshow('DETECCION Y SEGMENTACION', anotaciones)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Liberar recursos
cap.release()
out.release()
cv2.destroyAllWindows()
