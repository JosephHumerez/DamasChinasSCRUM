def crear_fichas_dos_jugadores():
    color_1 = "Rojo"
    color_2 = "Verde"
    coordenadas_rojas = [f'R_{i}' for i in range(1, 11)] 
    
    coordenadas_verdes = [f'V_{i}' for i in range(1, 11)] 
    
    tablero = {}
    for coord in coordenadas_rojas:
        tablero[coord] = color_1
    for coord in coordenadas_verdes:
        tablero[coord] = color_2
    return tablero

fichas_dos_jugadores = crear_fichas_dos_jugadores()

print(f"Total de fichas creadas: {len(fichas_dos_jugadores)}") 
print(f"Número de fichas Rojas: {list(fichas_dos_jugadores.values()).count('Rojo')}")
print("\nDisposición inicial (ejemplo):")
print(f"Posición R_1: {fichas_dos_jugadores.get('R_1')}")
print(f"Posición V_5: {fichas_dos_jugadores.get('V_5')}")

# Puntos Clave para Adaptar la Función
# Coordenadas Esenciales: Lo más importante es que las claves del diccionario (como 'R_1', 'V_10') coincidan con el sistema de coordenadas que usaste para construir tu tablero.
# Si tu tablero usa coordenadas de cuadrícula, podrías tener algo como tablero[(0, 4)] = "Rojo".
# Total de Fichas: Esta función genera 20 fichas en total (10 de cada color).
# Inicio del Juego: Los jugadores comenzarán a mover sus fichas desde su punta inicial (Rojo o Verde) hacia la punta opuesta (la del otro jugador).