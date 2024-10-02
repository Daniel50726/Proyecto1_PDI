import cv2
import numpy as np

# Inicialización de la cámara
cam = cv2.VideoCapture(0)
cv2.namedWindow('Colour Detection')  # Ventana para mostrar la detección de color


# Función vacía para usar en las trackbars (es requerida, aunque no se use)
def nothing(x):
    pass


# Crear barras deslizantes (trackbars) para ajustar los valores de Hue, Saturation y Value (HSV)
cv2.createTrackbar('Hue', 'Colour Detection', 0, 179, nothing)
cv2.createTrackbar('Saturation', 'Colour Detection', 0, 255, nothing)
cv2.createTrackbar('Value', 'Colour Detection', 0, 255, nothing)

# Bucle principal para el procesamiento de video
while True:
    ret, img = cam.read()  # Capturar la imagen de la cámara
    if not ret:
        break  # Si no se recibe la imagen, salir del bucle

    img = np.flip(img, axis=1)  # Voltear la imagen horizontalmente (efecto espejo)
    img = cv2.resize(img, (480, 360))  # Redimensionar la imagen para mejorar el rendimiento

    # Convertir la imagen de BGR a HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Aplicar desenfoque gaussiano para suavizar la imagen y reducir ruido
    blurred = cv2.GaussianBlur(hsv, (11, 11), 0)

    # Obtener los valores actuales de las barras deslizantes para H, S, V
    h = cv2.getTrackbarPos('Hue', 'Colour Detection')
    s = cv2.getTrackbarPos('Saturation', 'Colour Detection')
    v = cv2.getTrackbarPos('Value', 'Colour Detection')

    # Definir el rango de color para la máscara basada en los valores H, S, V seleccionados
    lower_colour = np.array([h, s, v])  # Color inferior del rango (ajustable con trackbars)
    upper_colour = np.array([180, 255, 255])  # Rango superior fijo (máximos valores HSV)

    # Crear una máscara que detecta solo los colores dentro del rango definido
    mask = cv2.inRange(hsv, lower_colour, upper_colour)

    # Aplicar la máscara sobre la imagen original para resaltar los colores detectados
    result = cv2.bitwise_and(img, img, mask=mask)

    # Mostrar la imagen con los colores detectados
    cv2.imshow('Colour Detection', result)

    # Salir si se presiona la tecla 'q'
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Liberar los recursos de la cámara y cerrar todas las ventanas
cam.release()
cv2.destroyAllWindows()
