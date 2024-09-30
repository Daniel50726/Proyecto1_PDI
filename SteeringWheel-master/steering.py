# Importando las librerías necesarias
import numpy as np  # Para manejar arrays y realizar operaciones numéricas
import cv2  # Para procesamiento de imágenes
import imutils  # Para funciones auxiliares de imágenes y video
from imutils.video import VideoStream  # Para capturar video desde la cámara
from directkeys import PressKey, A, D, Space, ReleaseKey  # Para emular las teclas del teclado

# Inicializa el stream de video desde la cámara
cam = VideoStream(src=0).start()  # Utiliza la cámara por defecto (ID 0)
currentKey = list()  # Lista para almacenar las teclas que están presionadas actualmente

# Bucle principal
while True:
    key_pressed = False  # Variable para rastrear si alguna tecla fue presionada

    # Capturar la imagen de la cámara y realizar ajustes de tamaño
    img = cam.read()  # Lee la imagen de la cámara
    img = np.flip(img, axis=1)  # Invierte la imagen horizontalmente para simular un espejo
    img = imutils.resize(img, width=640)  # Redimensiona la imagen a un ancho de 640 píxeles
    img = imutils.resize(img, height=480)  # Redimensiona la imagen a una altura de 480 píxeles

    # Convertir la imagen de BGR a HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Aplicar un desenfoque gaussiano para suavizar la imagen
    blurred = cv2.GaussianBlur(hsv, (11, 11), 0)

    # Definir el rango de color que queremos detectar (en el espacio HSV)
    colourLower = np.array([22, 107, 172])  # Limite inferior para el color
    colourUpper = np.array([180, 255, 255])  # Límite superior para el color

    # Obtener las dimensiones de la imagen (alto y ancho)
    height, width = img.shape[:2]

    # Crear una máscara para filtrar los colores dentro del rango especificado
    mask = cv2.inRange(blurred, colourLower, colourUpper)

    # Aplicar operaciones morfológicas para eliminar ruido (apertura y cierre)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))  # Remueve ruido
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))  # Cierra pequeños agujeros

    # Dividir la imagen en dos regiones de interés: parte superior e inferior
    upContour = mask[0:height//2, 0:width]  # Región superior (para el control de dirección)
    #downContour = mask[3*height//4:height, 2*width//5:3*width//5]  # Región inferior (para el control de "nitro")

    # Encontrar contornos en ambas regiones
    cnts_up = cv2.findContours(upContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_up = imutils.grab_contours(cnts_up)  # Convertir en formato utilizable

    #cnts_down = cv2.findContours(downContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cnts_down = imutils.grab_contours(cnts_down)

    # Si se detecta un contorno en la parte superior (decidir dirección del coche)
    if len(cnts_up) > 0:
        c = max(cnts_up, key=cv2.contourArea)  # Encuentra el contorno más grande
        M = cv2.moments(c)  # Calcula los momentos para encontrar el centroide
        cX = int(M["m10"] / (M["m00"] + 0.000001))  # Evitar división por cero

        # Determinar la dirección del coche basado en la posición del objeto
        if cX < (width // 2 - 35):  # Si el centroide está a la izquierda
            PressKey(A)  # Presiona la tecla 'A' para girar a la izquierda
            key_pressed = True
            currentKey.append(A)
        elif cX > (width // 2 + 35):  # Si el centroide está a la derecha
            PressKey(D)  # Presiona la tecla 'D' para girar a la derecha
            key_pressed = True
            currentKey.append(D)

    # Si se detecta un contorno en la parte inferior (activar "nitro")
    '''
    if len(cnts_down) > 0:
        PressKey(Space)  # Presiona la tecla 'Space' para activar "nitro"
        key_pressed = True
        currentKey.append(Space)
    '''

    # Dibujar rectángulos y etiquetas para las zonas de control en la imagen
    img = cv2.rectangle(img, (0, 0), (width // 2 - 35, height), (0, 255, 0), 1)
    cv2.putText(img, 'LEFT', (110, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))  # Zona izquierda

    img = cv2.rectangle(img, (width // 2 + 35, 0), (width, height), (0, 255, 0), 1)
    cv2.putText(img, 'RIGHT', (440, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))  # Zona derecha

    #img = cv2.rectangle(img, (2 * (width // 5), 3 * (height // 4)), (3 * width // 5, height), (0, 255, 0), 1)
    #cv2.putText(img, 'NITRO', (2 * (width // 5) + 20, height - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))  # Zona nitro

    # Mostrar la imagen procesada con las zonas dibujadas
    cv2.imshow("Steering", img)

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
