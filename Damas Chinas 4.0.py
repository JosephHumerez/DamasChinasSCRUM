import pygame
import sys
import math

class Tablero:
    def __init__(self):
        self.posiciones = self.crear_tablero_estrella()
        self.piezas = self.inicializar_piezas()

    def crear_tablero_estrella(self):
        # Genera las posiciones del tablero en forma de estrella
        posiciones = {}
        centro_x, centro_y = 300, 340
        espaciado = 25

        datos_fila = [
            (1, 0),
            (2, -0.5),
            (3, -1),
            (4, -1.5),
            (13, -6),
            (12, -5.5),
            (11, -5),
            (10, -4.5),
            (9, -4),
            (10, -4.5),
            (11, -5),
            (12, -5.5),
            (13, -6),
            (4, -1.5),
            (3, -1),
            (2, -0.5),
            (1, 0),
        ]

        id_pos = 0
        for indice_fila, (cantidad, mult_desplazamiento_x) in enumerate(datos_fila):
            desplazamiento_y = (indice_fila - 8) * espaciado * math.sqrt(3) / 2
            inicio_x = centro_x + mult_desplazamiento_x * espaciado

            for col in range(cantidad):
                x = inicio_x + col * espaciado
                y = centro_y + desplazamiento_y
                posiciones[id_pos] = (x, y)
                id_pos += 1

        return posiciones

    def inicializar_piezas(self):
        # Coloca las piezas iniciales de ambos jugadores
        piezas = {}

        piezas[0] = 1
        piezas[1] = 1
        piezas[2] = 1
        piezas[3] = 1
        piezas[4] = 1
        piezas[5] = 1
        piezas[6] = 1
        piezas[7] = 1
        piezas[8] = 1
        piezas[9] = 1

        piezas[111] = 2
        piezas[112] = 2
        piezas[113] = 2
        piezas[114] = 2
        piezas[115] = 2
        piezas[116] = 2
        piezas[117] = 2
        piezas[118] = 2
        piezas[119] = 2
        piezas[120] = 2

        return piezas

    def obtener_vecinos(self, id_pos):
        # Devuelve las posiciones vecinas a una casilla
        vecinos = []
        x, y = self.posiciones[id_pos]

        for otro_id, (ox, oy) in self.posiciones.items():
            if otro_id != id_pos:
                distancia = math.sqrt((x - ox)**2 + (y - oy)**2)
                if 22 < distancia < 32:
                    vecinos.append(otro_id)

        return vecinos

    def es_movimiento_valido(self, pos_origen, pos_destino, jugador_actual):
        # Verifica si el movimiento es válido para el jugador actual
        if pos_origen not in self.piezas:
            return False

        if self.piezas[pos_origen] != jugador_actual:
            return False

        if pos_destino in self.piezas:
            return False

        vecinos = self.obtener_vecinos(pos_origen)
        if pos_destino in vecinos:
            return True

        return self.puede_saltar(pos_origen, pos_destino, jugador_actual, set())

    def puede_saltar(self, pos_origen, pos_destino, jugador_actual, visitados):
        # Permite saltar solo sobre fichas propias
        if pos_origen in visitados:
            return False

        visitados.add(pos_origen)

        fx, fy = self.posiciones[pos_origen]
        vecinos = self.obtener_vecinos(pos_origen)

        for pos_intermedia in vecinos:
            if pos_intermedia in self.piezas and self.piezas[pos_intermedia] == jugador_actual:
                mx, my = self.posiciones[pos_intermedia]
                dx, dy = mx - fx, my - fy
                objetivo_x, objetivo_y = mx + dx, my + dy

                for id_candidato, (cx, cy) in self.posiciones.items():
                    if id_candidato not in self.piezas:
                        distancia = math.sqrt((cx - objetivo_x)**2 + (cy - objetivo_y)**2)
                        if distancia < 5:
                            if id_candidato == pos_destino:
                                return True

                            if self.puede_saltar(id_candidato, pos_destino, jugador_actual, visitados.copy()):
                                return True

        return False

    def mover_pieza(self, pos_origen, pos_destino):
        # Mueve la pieza si el movimiento es válido
        if pos_origen in self.piezas:
            jugador = self.piezas[pos_origen]
            del self.piezas[pos_origen]
            self.piezas[pos_destino] = jugador
            return True
        return False

    def verificar_ganador(self):
        # Verifica si algún jugador ganó
        casa_jugador1 = {111, 112, 113, 114, 115, 116, 117, 118, 119, 120}
        casa_jugador2 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

        jugador1_completo = all(
            pos in self.piezas and self.piezas[pos] == 1
            for pos in casa_jugador1
        )

        jugador2_completo = all(
            pos in self.piezas and self.piezas[pos] == 2
            for pos in casa_jugador2
        )

        if jugador1_completo:
            return 1
        if jugador2_completo:
            return 2

        return None


class Juego:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.tablero = Tablero()
        self.jugador_actual = 1
        self.pieza_seleccionada = None
        self.ganador = None

        # Colores y fuentes para la interfaz
        self.COLORES = {
            'fondo': (240, 235, 220),
            'tablero': (139, 90, 60),
            'casilla': (210, 180, 140),
            'jugador1': (220, 20, 60),
            'jugador2': (30, 144, 255),
            'seleccionado': (255, 215, 0),
            'movimiento_valido': (144, 238, 144),
            'texto': (50, 50, 50),
            'fondo_ganador': (255, 255, 255)
        }

        self.fuente = pygame.font.Font(None, 28)
        self.fuente_titulo = pygame.font.Font(None, 38)
        self.fuente_ganador = pygame.font.Font(None, 48)

    def manejar_evento(self, evento):
        # Controla los clics del usuario
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.ganador:
                return

            raton_x, raton_y = evento.pos
            pos_clickeada = self.obtener_posicion_en_raton(raton_x, raton_y)

            if pos_clickeada is not None:
                if self.pieza_seleccionada is None:
                    # Permite seleccionar cualquier ficha, sin importar el jugador
                    if pos_clickeada in self.tablero.piezas:
                        self.pieza_seleccionada = pos_clickeada
                else:
                    if pos_clickeada == self.pieza_seleccionada:
                        self.pieza_seleccionada = None
                    elif self.tablero.es_movimiento_valido(self.pieza_seleccionada, pos_clickeada, self.jugador_actual):
                        self.tablero.mover_pieza(self.pieza_seleccionada, pos_clickeada)
                        self.pieza_seleccionada = None

                        ganador = self.tablero.verificar_ganador()
                        if ganador:
                            self.ganador = ganador
                        else:
                            self.jugador_actual = 2 if self.jugador_actual == 1 else 1
                    else:
                        self.pieza_seleccionada = None

    def obtener_posicion_en_raton(self, raton_x, raton_y):
        # Devuelve el id de la casilla clickeada
        for id_pos, (x, y) in self.tablero.posiciones.items():
            distancia = ((raton_x - x) ** 2 + (raton_y - y) ** 2) ** 0.5
            if distancia <= 11:
                return id_pos
        return None

    def dibujar(self):
        # Dibuja todo el juego en pantalla
        self.pantalla.fill(self.COLORES['fondo'])

        texto_titulo = self.fuente_titulo.render("Damas Chinas", True, self.COLORES['texto'])
        rect_titulo = texto_titulo.get_rect(center=(400, 40))
        self.pantalla.blit(texto_titulo, rect_titulo)

        for id_pos in self.tablero.posiciones:
            self.dibujar_casilla(id_pos)

        for id_pos in self.tablero.posiciones:
            if id_pos in self.tablero.piezas:
                self.dibujar_pieza(id_pos)

        if self.pieza_seleccionada is not None:
            self.dibujar_movimientos_validos()

        self.dibujar_info_juego()

        if self.ganador:
            self.dibujar_ganador()

    def dibujar_casilla(self, id_pos):
        # Dibuja una casilla del tablero
        x, y = self.tablero.posiciones[id_pos]
        pygame.draw.circle(self.pantalla, self.COLORES['casilla'], (int(x), int(y)), 9)
        pygame.draw.circle(self.pantalla, self.COLORES['tablero'], (int(x), int(y)), 9, 2)

    def dibujar_pieza(self, id_pos):
        # Dibuja una pieza de jugador
        x, y = self.tablero.posiciones[id_pos]
        jugador = self.tablero.piezas[id_pos]
        color = self.COLORES['jugador1'] if jugador == 1 else self.COLORES['jugador2']

        if id_pos == self.pieza_seleccionada:
            pygame.draw.circle(self.pantalla, self.COLORES['seleccionado'], (int(x), int(y)), 12, 3)

        pygame.draw.circle(self.pantalla, color, (int(x), int(y)), 9)
        pygame.draw.circle(self.pantalla, (0, 0, 0), (int(x), int(y)), 9, 2)

    def dibujar_movimientos_validos(self):
        # Resalta las casillas donde puedes mover la pieza seleccionada
        for id_pos in self.tablero.posiciones:
            if id_pos not in self.tablero.piezas:
                if self.tablero.es_movimiento_valido(self.pieza_seleccionada, id_pos, self.jugador_actual):
                    x, y = self.tablero.posiciones[id_pos]
                    pygame.draw.circle(self.pantalla, self.COLORES['movimiento_valido'], (int(x), int(y)), 6)

    def dibujar_info_juego(self):
        # Muestra el turno actual
        texto_jugador = f"Turno: Jugador {self.jugador_actual}"
        color_circulo = self.COLORES['jugador1'] if self.jugador_actual == 1 else self.COLORES['jugador2']

        superficie_texto = self.fuente.render(texto_jugador, True, self.COLORES['texto'])
        rect_texto = superficie_texto.get_rect(center=(300, 670))
        self.pantalla.blit(superficie_texto, rect_texto)

        pygame.draw.circle(self.pantalla, color_circulo, (220, 670), 9)
        pygame.draw.circle(self.pantalla, (0, 0, 0), (220, 670), 9, 2)

    def dibujar_ganador(self):
        # Muestra el mensaje de ganador
        capa = pygame.Surface((600, 680))
        capa.set_alpha(200)
        capa.fill((0, 0, 0))
        self.pantalla.blit(capa, (0, 0))

        texto_ganador = f"¡Jugador {self.ganador} Gana!"
        superficie_texto = self.fuente_ganador.render(texto_ganador, True, self.COLORES['fondo_ganador'])
        rect_texto = superficie_texto.get_rect(center=(300, 340))
        self.pantalla.blit(superficie_texto, rect_texto)

def main():
    pygame.init()

    ANCHO_VENTANA = 600
    ALTO_VENTANA = 680

    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Damas Chinas")

    reloj = pygame.time.Clock()
    juego = Juego(pantalla)

    ejecutando = True
    while ejecutando:
        reloj.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            juego.manejar_evento(evento)

        juego.dibujar()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()