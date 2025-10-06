import pygame
import sys
import math

# Inicializar pygame
pygame.init()

# Configuración ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Damas Chinas - 2 Jugadores")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 50, 50)
AZUL = (50, 50, 200)
GRIS = (200, 200, 200)
COLOR_FONDO_MENSAJE = GRIS

# Fuente para el mensaje de turno
FUENTE_TURNO = pygame.font.SysFont(None, 30)

# Parámetros de casillas
RADIO = 20
ESPACIO = 50

# Variables de turno
turno = 1  # Jugador 1 empieza

# Clases
class Casilla:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ocupada_por = 0  # 0 = libre, 1 = Jugador 1, 2 = Jugador 2

    def dibujar(self, ventana):
        color = NEGRO
        pygame.draw.circle(ventana, color, (self.x, self.y), RADIO, 1)
        if self.ocupada_por == 1:
            pygame.draw.circle(ventana, ROJO, (self.x, self.y), RADIO-4)
        elif self.ocupada_por == 2:
            pygame.draw.circle(ventana, AZUL, (self.x, self.y), RADIO-4)

class Ficha:
    def __init__(self, casilla):
        self.casilla = casilla

# Generar tablero simple 2 jugadores (triángulos enfrentados)
casillas = []
filas = 4
centro_x, centro_y = ANCHO//2, ALTO//2

# Triángulo Jugador 1
for fila in range(filas):
    for i in range(fila + 1):
        x = centro_x - fila*ESPACIO//2 + i*ESPACIO
        y = centro_y - 3*ESPACIO + fila*ESPACIO
        casilla = Casilla(x, y)
        casilla.ocupada_por = 1
        casillas.append(casilla)

# Triángulo Jugador 2
for fila in range(filas):
    for i in range(fila + 1):
        x = centro_x - fila*ESPACIO//2 + i*ESPACIO
        y = centro_y + 3*ESPACIO - fila*ESPACIO
        casilla = Casilla(x, y)
        casilla.ocupada_por = 2
        casillas.append(casilla)

# Función para mostrar mensaje de turno
def mostrar_turno(jugador):
    texto = f"Ahora es el turno del Jugador {jugador}"
    superficie_texto = FUENTE_TURNO.render(texto, True, NEGRO)
    cuadro = pygame.Surface((superficie_texto.get_width()+10, superficie_texto.get_height()+10))
    cuadro.fill(COLOR_FONDO_MENSAJE)
    cuadro.blit(superficie_texto, (5,5))
    VENTANA.blit(cuadro, (ANCHO - cuadro.get_width() - 10, 10))

# Función para detectar clic en casilla
def casilla_clic(pos):
    for c in casillas:
        dx = pos[0] - c.x
        dy = pos[1] - c.y
        if math.hypot(dx, dy) <= RADIO:
            return c
    return None

# Variables de selección
ficha_seleccionada = None

# Bucle principal
while True:
    VENTANA.fill(BLANCO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clic = pygame.mouse.get_pos()
            casilla = casilla_clic(clic)
            if casilla:
                if ficha_seleccionada is None:
                    # Seleccionar ficha propia
                    if casilla.ocupada_por == turno:
                        ficha_seleccionada = casilla
                else:
                    # Mover ficha seleccionada a casilla vacía adyacente
                    if casilla.ocupada_por == 0:
                        dx = abs(casilla.x - ficha_seleccionada.x)
                        dy = abs(casilla.y - ficha_seleccionada.y)
                        if dx <= ESPACIO+5 and dy <= ESPACIO+5:
                            # Movimiento válido simple
                            casilla.ocupada_por = turno
                            ficha_seleccionada.ocupada_por = 0
                            ficha_seleccionada = None
                            # Cambiar turno
                            turno = 2 if turno == 1 else 1

    # Dibujar casillas
    for c in casillas:
        c.dibujar(VENTANA)

    # Mostrar mensaje de turno
    mostrar_turno(turno)

    pygame.display.flip()
