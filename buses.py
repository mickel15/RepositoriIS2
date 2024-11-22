import cv2
import pytesseract
import difflib
from datetime import datetime
import pyodbc
import pywhatkit as kit

def find_most_similar_word(target_word, word_list):
    """
    Encuentra la palabra más similar a target_word en word_list.
    """
    similarities = [(word, difflib.SequenceMatcher(None, target_word, word).ratio()) for word in word_list]
    most_similar_word, similarity_score = max(similarities, key=lambda x: x[1])
    return most_similar_word, similarity_score

def insert_detection_to_db(cursor, extracted_text, most_similar_word, similarity_score, bus_route, detection_time):
    """
    Inserta la detección en la base de datos.
    """
    cursor.execute("""
        INSERT INTO Detecciones (TextoExtraido, PalabraSimilar, PuntajeSimilitud, RutaBus, HoraDeteccion)
        VALUES (?, ?, ?, ?, ?)
    """, (extracted_text, most_similar_word, similarity_score, bus_route, detection_time))

def send_whatsapp_message(phone_number, message):
    """
    Envía un mensaje de WhatsApp usando pywhatkit.
    """
    kit.sendwhatmsg_instantly(phone_number, message)

# Cambiar directorio donde está instalado tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Configuración adicional de pytesseract para mejorar la precisión
custom_config = r'--oem 3 --psm 6'

# Conectar a SQL Server con autenticación de Windows
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-B2C5UKG\SQLEXPRESS;'
    r'DATABASE=Proyecto JIC;'
    r'Trusted_Connection=yes;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Capturar video desde la cámara
cap = cv2.VideoCapture(0)

# Número de teléfono al que se enviará el mensaje (incluye el código de país)
phone_number = "+50762352493"  # Reemplaza con el número de teléfono correcto

while True:
    # Capturar un cuadro de video
    ret, frame = cap.read()
    
    if not ret:
        print("Error al capturar el cuadro de video")
        break

    # Definir la región de interés (ROI) donde se espera que esté el texto del título del bus
    # Ajusta estos valores dependiendo de la ubicación exacta del texto en el cuadro de video
    height, width, _ = frame.shape
    roi_top_left_x = 50
    roi_top_left_y = 50
    roi_bottom_right_x = width - 50
    roi_bottom_right_y = height - 50
    roi = frame[roi_top_left_y:roi_bottom_right_y, roi_top_left_x:roi_bottom_right_x]

    # Dibujar un rectángulo en el cuadro de video para mostrar la región de interés
    cv2.rectangle(frame, (roi_top_left_x, roi_top_left_y), (roi_bottom_right_x, roi_bottom_right_y), (0, 255, 0), 2)

    # Convertir imagen a escala de grises
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Aplicar suavizado para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplicar umbral para convertir a imagen binaria
    _, threshold_img = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Aplicar operaciones morfológicas para mejorar la calidad de la imagen binaria
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph_img = cv2.morphologyEx(threshold_img, cv2.MORPH_CLOSE, kernel)

    try:
        # Pasar la imagen a través de pytesseract
        extracted_text = pytesseract.image_to_string(morph_img, config=custom_config)

        # Lista de palabras para comparar
        words_to_compare = ['4B-1010','4B-0586','4B-1001','4B-0285','4B-1007',
                            '4B-0541','4B-0559','4B-0917','4B-0478','4B-0216',
                            '4B-0160','4B-0080','4B-0394','4B-0127','4B-0249',
                            '4B-0512','4B-0172']

        # Comparar palabras y encontrar la más similar
        most_similar_word, similarity_score = find_most_similar_word(extracted_text, words_to_compare)
        
        # Imprimir solo si la similitud es del 60% o más
        if similarity_score >= 0.6:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Texto extraído:", extracted_text)
            print("Palabra más similar:", most_similar_word)
            print("Puntaje de similitud:", similarity_score)
            
            # Imprimir que el bus es de ARMUELLES DAVID si la palabra más similar es "4B-0463"
            bus_routes = {
                "4B-1010": "NATA DAVID",
                "4B-0586": "SOLOY DAVID",
                "4B-1001": "SAN FELIX DAVID",
                "4B-0285": "PALMIRA DAVID",
                "4B-1007": "SAN LORENZO DAVID",
                "4B-0541": "COCHEA DAVID",
                "4B-0559": "PORTON DAVID",
                "4B-0917": "AGUACATAL DAVID",
                "4B-0478": "SERENO DAVID",
                "4B-0216": "DIVALA DAVID",
                "4B-0160": "ARMUELLES DAVID",
                "4B-0080": "ARMUELLES DAVID",
                "4B-0394": "DOLEGA DAVID",
                "4B-0127": "FRONTERA DAVID",
                "4B-0249": "FRONTERA DAVID",
                "4B-0512": "ARMUELLES DAVID",
                "4B-0172": "ZONA URBANA"
            }
            
            if most_similar_word in bus_routes:
                bus_route = bus_routes[most_similar_word]
                print(f"El bus es de {bus_route}")
                print("Hora de detección:", current_time)
                
                # Insertar la detección en la base de datos
                insert_detection_to_db(cursor, extracted_text, most_similar_word, similarity_score, bus_route, current_time)
                conn.commit()

                # Enviar mensaje de WhatsApp
                message = f"El bus de {bus_route} acaba de pasar por Boquerón a las {current_time}."
                send_whatsapp_message(phone_number, message)

    except Exception as e:
        print(f"Error durante la extracción de texto: {e}")

    # Mostrar la imagen con el rectángulo dibujado
    cv2.imshow("Frame", frame)

    # Esperar a que se presione 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

# Cerrar la conexión a la base de datos
conn.close()
