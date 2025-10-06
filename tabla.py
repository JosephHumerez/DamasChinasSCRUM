import pygame
import sys

class Tablero17x17:
    def init(self):
        self.filas = 17
        self.columnas = 17
        self.tamano_casilla = 40
        self.ancho_tablero = self.columnas * self.tamano_casilla
        self.alto_tablero = self.filas * self.tamano_casilla
        
        # Colores
        self.COLOR_BLANCO = (255, 255, 255)
        self.COLOR_GRIS = (200, 200, 200)
        self.COLOR_LINEA = (150, 150, 150)
        
        # Matriz para almacenar estado del tablero
        self.tablero = [[None for _ in range(self.columnas)] for _ in range(self.filas)]
    
    def dibujar_tablero(self, pantalla):
        """
        Dibuja el tablero de 17x17 casillas en la pantalla
        """
       
        pantalla.fill(self.COLOR_BLANCO)
        
        
        for fila in range(self.filas):
            for col in range(self.columnas):
                x = col * self.tamano_casilla
                y = fila * self.tamano_casilla
                
                # Dibuja rectángulo para cada casilla
                rect = pygame.Rect(x, y, self.tamano_casilla, self.tamano_casilla)
                pygame.draw.rect(pantalla, self.COLOR_BLANCO, rect)
                pygame.draw.rect(pantalla, self.COLOR_LINEA, rect, 1)
    
    def obtener_posicion(self, pos_mouse):
        """
        Convierte coordenadas del mouse a posición de fila, columna
        """
        x, y = pos_mouse
        col = x // self.tamano_casilla
        fila = y // self.tamano_casilla
        
        if 0 <= fila < self.filas and 0 <= col < self.columnas:
            return fila, col
        return None, None
    
    def obtener_coordenadas_pixel(self, fila, col):
        """
        Convierte fila, columna a coordenadas de pixel (centro de la casilla)
        """
        x = col * self.tamano_casilla + self.tamano_casilla // 2
        y = fila * self.tamano_casilla + self.tamano_casilla // 2
        return x, y