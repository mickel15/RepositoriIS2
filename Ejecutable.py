# Importar librerías
from ultralytics import YOLO
import cv2

# Instanciar el modelo YOLO
model = YOLO('best.pt')

# Videocaptura
cap = cv2.VideoCapture(0)

while True:
    # Captura de frame
    ret, frame = cap.read()

    # Predecir utilizando el modelo
    resultados = model(frame, imgsz=640, conf =0.30)

    # Verificar si hay detecciones
    if len(resultados) > 0:
        # Renderizar el primer resultado
        annotated_frame = resultados[0].plot()

        # Mostrar los fotogramas
        cv2.imshow('DETECCION Y SEGMENTACION', annotated_frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
