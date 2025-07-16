from Tablero import NUM_CASILLAS_EXTERNAS, ENTRADAS_LLEGADA, SALIDAS_JUGADORES, inicializar_tablero, inicializar_zonas_llegada, es_casilla_segura
from Logica import inicializar_jugadores_data, actualizar_turno
import random
def main():
    tablero_externo = inicializar_tablero()
    zonas_llegada = inicializar_zonas_llegada()

    jugadores = {}

    orden_turnos = []

    colores_disponibles = ["rojo", "verde", "amarillo", "azul"]
    num_jugadores = 0
    while num_jugadores < 2 or num_jugadores > 4:
        try:
            num_jugadores = int(input("¿Cuántos jugadores (2-4)? "))
        except ValueError:
            print("Por favor, ingresa un número válido.")

    for i in range(num_jugadores):
        color_elegido = colores_disponibles[i]

        nombre_jugador = input(f"Jugador {i+1} ({color_elegido.capitalize()}): Ingresa tu nombre: ")

        jugadores[color_elegido] = inicializar_jugadores_data(color_elegido, nombre_jugador)
        orden_turnos.append(color_elegido) 


if __name__ == "__main__":
    main()