"""
Proyecto 1 de PDI
Presentado por los estudiantes:
             Jorge Sebastian Arroyo Estrada     sebastian.arroyo1@udea.edu.co
             CC:1193482707
             Daniel Felipe Yépez Taimal         daniel.yepez@udea.edu.co
             CC:1004193180
Proposito: Profundizar y aplicar los conceptos de PDI en un juego interactivo
"""

import ctypes
import time

# Definir la función SendInput para enviar entradas de teclado/mouse a través de la API de Windows
SendInput = ctypes.windll.user32.SendInput

# Definir los códigos de teclado escaneados para las teclas que se desean simular
#W = 0x11  # Código para la tecla 'W'
A = 0x1E  # Código para la tecla 'A'
#S = 0x1F  # Código para la tecla 'S'
D = 0x20  # Código para la tecla 'D'

# Redefinir la estructura de teclado (KeyBdInput) en formato C para usarla con ctypes
PUL = ctypes.POINTER(ctypes.c_ulong)  # Tipo de puntero para los campos de información extra

class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),      # Código virtual de la tecla (no usado aquí)
        ("wScan", ctypes.c_ushort),    # Código del escaneo físico de la tecla
        ("dwFlags", ctypes.c_ulong),   # Banderas para indicar si es una tecla presionada o liberada
        ("time", ctypes.c_ulong),      # Tiempo de la pulsación (usualmente 0)
        ("dwExtraInfo", PUL)           # Información extra (puntero)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

# Unión que agrupa las diferentes estructuras posibles para el envío de inputs
class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBdInput),    # Teclado
        ("mi", MouseInput),    # Ratón
        ("hi", HardwareInput)  # Hardware
    ]

# Estructura principal que contiene el tipo de input y la unión anterior
class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),  # Tipo de entrada (teclado, ratón, etc.)
        ("ii", Input_I)            # Input específico según el tipo
    ]

# Función para simular la presión de una tecla
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)  # Campo de información extra
    ii_ = Input_I()
    # Configuración del input de teclado para presionar una tecla
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))  # 0x0008: Key Press
    x = Input(ctypes.c_ulong(1), ii_)  # 1 es el tipo de input para teclado
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))  # Enviar el input

# Función para simular la liberación de una tecla
def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)  # Campo de información extra
    ii_ = Input_I()
    # Configuración del input de teclado para liberar una tecla
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))  # 0x0002: Key Release
    x = Input(ctypes.c_ulong(1), ii_)  # 1 es el tipo de input para teclado
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))  # Enviar el input

# Código de prueba que presiona y luego libera la tecla 'W'
'''
if __name__ == '__main__':
    PressKey(W)  # Simular la presión de la tecla 'W'
    time.sleep(1)  # Esperar 1 segundo con la tecla presionada
    ReleaseKey(W)  # Simular la liberación de la tecla 'W'
    time.sleep(1)  # Esperar 1 segundo antes de finalizar
'''