import pygame
import sys

# Inicializar pygame
pygame.init()

# Ventana principal
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mensaje de turno - Prototipo")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)

# Fuente
FUENTE = pygame.font.SysFont(None, 30)

# Variables de turno
turno = 1
mostrar_mensaje = False
mensaje_tiempo = 2000  # ms que se muestra el mensaje
timer_event = pygame.USEREVENT + 1

# Función para dibujar mensaje en esquina superior derecha
def dibujar_mensaje():
    texto = f"Turno del Jugador {turno}"
    superficie = FUENTE.render(texto, True, NEGRO)
    cuadro = pygame.Surface((superficie.get_width()+10, superficie.get_height()+10))
    cuadro.fill(GRIS)
    cuadro.blit(superficie, (5,5))
    # Mostrar en esquina superior derecha
    VENTANA.blit(cuadro, (ANCHO - cuadro.get_width() - 10, 10))

# Bucle principal
while True:
    VENTANA.fill(BLANCO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            # Presioné cualquier tecla o click
            mostrar_mensaje = True
            pygame.time.set_timer(timer_event, mensaje_tiempo)  # activar timer
        elif event.type == timer_event:
            # Pasó tiempo para ocultar el mensaje
            mostrar_mensaje = False
            # Cambiar turno
            turno = 2 if turno == 1 else 1
            pygame.time.set_timer(timer_event, 0)  # desactivar timer

    # Dibujar mensaje si corresponde
    if mostrar_mensaje:
        dibujar_mensaje()

    pygame.display.flip()
