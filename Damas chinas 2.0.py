import pygame
import sys
import math

# Inicializar pygame
pygame.init()

# Configuración ventana
ANCHO, ALTO = 800, 800
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Damas Chinas - Estrella 2 Jugadores")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 50, 50)
AZUL = (50, 50, 200)
GRIS = (200, 200, 200)

# Fuente mensaje turno
FUENTE_TURNO = pygame.font.SysFont(None, 30)
MARGEN = 10

# Parámetros de casilla
RADIO = 15
ESPACIO = 35  # distancia entre casillas

# Variables de turno
turno = 1

# Clases
class Casilla:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ocupada_por = 0  # 0 libre, 1 jugador1, 2 jugador2

    def dibujar(self, ventana):
        pygame.draw.circle(ventana, NEGRO, (self.x, self.y), RADIO, 1)
        if self.ocupada_por == 1:
            pygame.draw.circle(ventana, ROJO, (self.x, self.y), RADIO-3)
        elif self.ocupada_por == 2:
            pygame.draw.circle(ventana, AZUL, (self.x, self.y), RADIO-3)

# Generar tablero estrella (simplificado, 2 jugadores)
casillas = []

# Centro del tablero
centro_x, centro_y = ANCHO//2, ALTO//2

# Triángulo superior (Jugador 1)
for fila in range(4):
    for i in range(fila + 1):
        x = centro_x - fila*ESPACIO//2 + i*ESPACIO
        y = centro_y - 6*ESPACIO + fila*ESPACIO
        c = Casilla(x, y)
        c.ocupada_por = 1
        casillas.append(c)

# Triángulo inferior (Jugador 2)
for fila in range(4):
    for i in range(fila + 1):
        x = centro_x - fila*ESPACIO//2 + i*ESPACIO
        y = centro_y + 6*ESPACIO - fila*ESPACIO
        c = Casilla(x, y)
        c.ocupada_por = 2
        casillas.append(c)

# Hexágono central (espacio libre)
for fila in range(-3, 4):
    for col in range(-3, 4):
        if abs(fila + col) <= 3:
            x = centro_x + col * ESPACIO
            y = centro_y + fila * ESPACIO * math.sqrt(3)/2
            # Evitar duplicar casillas de triángulos iniciales
            if not any(math.hypot(x-c.x, y-c.y)<1 for c in casillas):
                casillas.append(Casilla(x, y))

# Función para mostrar turno
def mostrar_turno(jugador):
    texto = f"Ahora es el turno del Jugador {jugador}"
    superficie = FUENTE_TURNO.render(texto, True, NEGRO)
    cuadro = pygame.Surface((superficie.get_width()+10, superficie.get_height()+10))
    cuadro.fill(GRIS)
    cuadro.blit(superficie, (5,5))
    VENTANA.blit(cuadro, (ANCHO - cuadro.get_width() - MARGEN, MARGEN))

# Detectar clic en casilla
def casilla_clic(pos):
    for c in casillas:
        if math.hypot(pos[0]-c.x, pos[1]-c.y) <= RADIO:
            return c
    return None

# Selección
ficha_seleccionada = None

# Bucle principal
while True:
    VENTANA.fill(BLANCO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            c = casilla_clic(pos)
            if c:
                if ficha_seleccionada is None:
                    if c.ocupada_por == turno:
                        ficha_seleccionada = c
                else:
                    # mover a casilla vacía adyacente
                    if c.ocupada_por == 0:
                        dx = abs(c.x - ficha_seleccionada.x)
                        dy = abs(c.y - ficha_seleccionada.y)
                        if dx <= ESPACIO+5 and dy <= ESPACIO+5:
                            c.ocupada_por = turno
                            ficha_seleccionada.ocupada_por = 0
                            ficha_seleccionada = None
                            turno = 2 if turno == 1 else 1

    # Dibujar todas las casillas
    for c in casillas:
        c.dibujar(VENTANA)

    # Mostrar turno
    mostrar_turno(turno)

    pygame.display.flip()
