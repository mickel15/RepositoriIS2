import customtkinter as ctk
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk
from ultralytics import YOLO

# Inicializamos el modelo YOLO con el archivo preentrenado 'best.pt'
model = YOLO('best.pt')

# Función para ejecutar el modelo YOLO en un video
def run_model_on_video(video_path):
    cap = cv2.VideoCapture(video_path)  # Abrir el video
    if not cap.isOpened():
        print("Error al abrir el archivo de video")
        return

    while cap.isOpened():
        ret, frame = cap.read()  # Leer cada frame del video
        if not ret:
            break

        results = model(frame)  # Ejecutar el modelo en el frame
        annotated_frame = results[0].plot()  # Anotar el frame con las detecciones

        cv2.imshow('Deteccion en video', annotated_frame)  # Mostrar el frame anotado

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Salir si se presiona 'q'
            break

    cap.release()
    cv2.destroyAllWindows()

# Función para ejecutar el modelo YOLO en la cámara en tiempo real
def run_model_on_camera():
    cap = cv2.VideoCapture(0)  # Abrir la cámara
    if not cap.isOpened():
        print("Error al abrir la camara")
        return

    while cap.isOpened():
        ret, frame = cap.read()  # Leer cada frame de la cámara
        if not ret:
            break

        results = model(frame)  # Ejecutar el modelo en el frame
        annotated_frame = results[0].plot()  # Anotar el frame con las detecciones

        cv2.imshow('Deteccion en camara', annotated_frame)  # Mostrar el frame anotado

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Salir si se presiona 'q'
            break

    cap.release()
    cv2.destroyAllWindows()

# Función para seleccionar un archivo de video y ejecutar el modelo en él
def select_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])  # Abrir diálogo para seleccionar video
    if video_path:
        run_model_on_video(video_path)  # Ejecutar el modelo en el video seleccionado

# Función para cambiar el color del botón al pasar el cursor
def on_enter(event, button):
    button.configure(fg_color="#005f73")  # Cambia el color al pasar el cursor

# Función para restaurar el color del botón cuando el cursor se aleja
def on_leave(event, button):
    button.configure(fg_color="#0077b6")  # Color original

# Configuración de la interfaz gráfica
ctk.set_appearance_mode("dark")  # Establecer modo oscuro
ctk.set_default_color_theme("blue")  # Establecer tema azul

# Crear la ventana principal
root = ctk.CTk()
root.title("YOLOv8 Detección de Buses")
root.geometry("800x600")  # Tamaño inicial de la ventana

# Crear un frame para contener los elementos
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Cargar la imagen del logo
logo_image = Image.open("logo.png")
logo_image = logo_image.resize((150, 150), Image.LANCZOS)  # Ajustar el tamaño del logo
logo_photo = ImageTk.PhotoImage(logo_image)

# Crear el label con la imagen del logo
logo_label = ctk.CTkLabel(master=frame, image=logo_photo, text="")
logo_label.pack(pady=10)

# Crear un label con texto
label = ctk.CTkLabel(master=frame, text="Seleccione una opción", font=("Arial", 16))
label.pack(pady=12, padx=10)

# Crear un frame para los botones
button_frame = ctk.CTkFrame(master=frame)
button_frame.pack(fill="both", expand=True, pady=10)

# Crear el botón para seleccionar un video y agregar eventos para cambiar el color
button_video = ctk.CTkButton(master=button_frame, text="Seleccionar Video", command=select_video, fg_color="#0077b6")
button_video.pack(side="top", fill="both", expand=True, pady=10, padx=10)
button_video.bind("<Enter>", lambda event, button=button_video: on_enter(event, button))
button_video.bind("<Leave>", lambda event, button=button_video: on_leave(event, button))

# Crear el botón para usar la cámara y agregar eventos para cambiar el color
button_camera = ctk.CTkButton(master=button_frame, text="Usar Cámara", command=run_model_on_camera, fg_color="#0077b6")
button_camera.pack(side="top", fill="both", expand=True, pady=10, padx=10)
button_camera.bind("<Enter>", lambda event, button=button_camera: on_enter(event, button))
button_camera.bind("<Leave>", lambda event, button=button_camera: on_leave(event, button))

# Ejecutar la ventana principal
root.mainloop()

