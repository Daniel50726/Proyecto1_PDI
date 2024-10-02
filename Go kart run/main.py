# Librerías
import numpy as np
import cv2  # Para procesamiento de imágenes
import imutils  # Para funciones auxiliares de imágenes y video
from imutils.video import VideoStream  # Para capturar video desde la cámara
from directkeys import PressKey, A, D, ReleaseKey  # Para emular las teclas del teclado
import time

# Inicializa el stream de video desde la cámara
cam = VideoStream(src=0).start()
currentKey = list()  # Lista para almacenar las teclas que están presionadas actualmente

# Define un temporizador para limitar la frecuencia de pulsación de teclas
last_pressed_time = time.time()  # Inicializa el tiempo de la última pulsación
key_press_interval = 0.02  # Intervalo de 0.8 segundos entre pulsaciones

# Bucle principal
while True:
    key_pressed = False  # Variable para rastrear si alguna tecla fue presionada

    # Capturar la imagen de la cámara y realizar ajustes de tamaño
    img = cam.read()  # Lee la imagen de la cámara
    img = np.flip(img, axis=1)  # Invierte la imagen horizontalmente para simular un espejo
    img = imutils.resize(img, width=640)
    img = imutils.resize(img, height=480)

    # Convertir la imagen de BGR a HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Aplicar un desenfoque gaussiano para suavizar la imagen
    blurred = cv2.GaussianBlur(hsv, (15,15), 0)

    # Definir el rango de color que queremos detectar (en el espacio HSV)
    colourLower = np.array([167, 150, 116])
    colourUpper = np.array([180, 255, 255])

    # Obtener las dimensiones de la imagen (alto y ancho)
    height, width = img.shape[:2]

    # Crear una máscara para filtrar los colores dentro del rango especificado
    mask = cv2.inRange(blurred, colourLower, colourUpper)

    # Aplicar operaciones morfológicas para eliminar ruido (apertura y cierre)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))  # Remueve ruido
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))  # Cierra pequeños agujeros

    cv2.imshow("Máscara", mask)

    # Detectar y procesar los bordes de los objetos dentro de la imagen.
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)  # Convertir en formato utilizable

    # Si se detecta un contorno en la imagen (decidir dirección del coche)
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)  # Encuentra el contorno más grande
        M = cv2.moments(c)  # Calcula los momentos para encontrar el centroide
        cX = int(M["m10"] / (M["m00"] + 0.000001))  # Evitar división por cero

        # Determinar la dirección del coche basado en la posición del objeto
        if time.time() - last_pressed_time > key_press_interval:  # Verifica si ha pasado suficiente tiempo
            if cX < (width // 2 - 35):  # Si el centroide está a la izquierda
                PressKey(A)  # Presiona la tecla 'A' para girar a la izquierda
                key_pressed = True
                currentKey.append(A)
            elif cX > (width // 2 + 35):  # Si el centroide está a la derecha
                PressKey(D)  # Presiona la tecla 'D' para girar a la derecha
                key_pressed = True
                currentKey.append(D)
            last_pressed_time = time.time()  # Actualiza el tiempo de la última pulsación

    # Dibujar rectángulos y etiquetas para las zonas de control en la imagen
    img = cv2.rectangle(img, (0, 0), (width // 2 - 35, height), (0, 255, 0), 1)
    cv2.putText(img, 'Izquierda', (80, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

    img = cv2.rectangle(img, (width // 2 + 35, 0), (width, height), (0, 255, 0), 1)
    cv2.putText(img, 'Derecha', (440, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

    # Mostrar la imagen procesada con las zonas dibujadas
    cv2.imshow("Go Kart Run", img)

    # Liberar teclas si no se ha presionado ninguna en esta iteración
    if not key_pressed and len(currentKey) != 0:
        for current in currentKey:
            ReleaseKey(current)
        currentKey.clear()

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar los recursos y cerrar todas las ventanas
cv2.destroyAllWindows()
