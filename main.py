from Tablero import NUM_CASILLAS_EXTERNAS, ENTRADAS_LLEGADA, SALIDAS_JUGADORES, inicializar_tablero, inicializar_zonas_llegada, es_casilla_segura, CASILLAS_SEGURAS, SALIDAS_JUGADORES 
from Interfaz import mostrar_tablero, pedir_opcion_movimiento 
from Logica import inicializar_jugadores_data, actualizar_turno, lanzar_dados, obtener_movimientos_posibles, mover_ficha, aplicar_bonus_movimiento
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
    MODO_DESARROLLADOR = False 

    juego_activo = True
    jugador_actual_idx = 0 
    while juego_activo:
        jugador_actual_color = orden_turnos[jugador_actual_idx]
        jugador_actual_data = jugadores[jugador_actual_color]

        print(f"\n--- Turno de {jugador_actual_color.capitalize()} ---")
        mostrar_tablero(tablero_externo, zonas_llegada, jugadores)

        dados_tirados = (0, 0) 
        if MODO_DESARROLLADOR:
            while True:
                try:
                    d1_input = input("Dado 1 (1-6, o 'r' para aleatorio): ").strip().lower()
                    dado1 = int(d1_input) if d1_input.isdigit() else lanzar_dados()[0]
                    if not (1 <= dado1 <= 6): raise ValueError
                    break
                except ValueError: print("Entrada inválida para Dado 1. Intenta de nuevo.")
            while True:
                try:
                    d2_input = input("Dado 2 (1-6, o 'r' para aleatorio): ").strip().lower()
                    dado2 = int(d2_input) if d2_input.isdigit() else lanzar_dados()[1]
                    if not (1 <= dado2 <= 6): raise ValueError
                    break
                except ValueError: print("Entrada inválida para Dado 2. Intenta de nuevo.")
            dados_tirados = (dado1, dado2)
        else:
            dados_tirados = lanzar_dados()

        print(f"Dados: {dados_tirados[0]}, {dados_tirados[1]}")
        dados_son_par = (dados_tirados[0] == dados_tirados[1])

      
        if dados_son_par:
            jugador_actual_data["pares_consecutivos"] += 1
        else:
            jugador_actual_data["pares_consecutivos"] = 0 

      
        if jugador_actual_data["pares_consecutivos"] == 3:
            print(f"¡{jugador_actual_color.capitalize()} ha sacado TRES PARES SEGUIDOS!")
            if jugador_actual_data["ultima_ficha_movida"] and \
               jugador_actual_data["ultima_ficha_movida"]["estado"] != "meta":
                ficha_a_carcel = jugador_actual_data["ultima_ficha_movida"]
                print(f"La ficha {ficha_a_carcel['jugador']}-{ficha_a_carcel['id']} va a la cárcel.")

                
                if ficha_a_carcel["estado"] == "en_juego":
                    tablero_externo[ficha_a_carcel["posicion"]].remove(ficha_a_carcel)
                elif ficha_a_carcel["estado"] == "llegada":
                    zonas_llegada[ficha_a_carcel["jugador"]][ficha_a_carcel["posicion"]] = None

                ficha_a_carcel["estado"] = "carcel"
                ficha_a_carcel["posicion"] = None
                jugador_actual_data["en_juego"] -= 1 
            else:
                print("No hay una ficha reciente que mover a la cárcel o ya está en la meta.")
            jugador_actual_data["pares_consecutivos"] = 0 

        fichas_en_carcel = [f for f in jugador_actual_data["fichas"] if f["estado"] == "carcel"]

        movimientos_dados = []
        if 5 in dados_tirados and fichas_en_carcel:
            print(f"Tienes un 5 y fichas en la cárcel. Debes sacar una ficha.")
            if dados_tirados[0] == 5:
                movimientos_dados.append((fichas_en_carcel[0], 5))
            elif dados_tirados[1] == 5 and dados_tirados[0] != 5: 
                 movimientos_dados.append((fichas_en_carcel[0], 5))


        else: 
            movimientos_dados = obtener_movimientos_posibles(jugador_actual_data, tablero_externo, zonas_llegada, dados_tirados)

        if not movimientos_dados:
            print("No hay movimientos válidos con los dados tirados.")
        else:
            ficha_a_mover_obj = None
            pasos_a_mover = 0

            if len(movimientos_dados) == 1:
                ficha_a_mover_obj, pasos_a_mover = movimientos_dados[0]
                print(f"Movimiento automático de {ficha_a_mover_obj['jugador']}-{ficha_a_mover_obj['id']} por {pasos_a_mover} pasos.")
            else:
                ficha_a_mover_obj, pasos_a_mover = pedir_opcion_movimiento(movimientos_dados)

            if ficha_a_mover_obj:
                movimiento_exitoso, bonus_captura, bonus_llegada = mover_ficha(
                    tablero_externo, zonas_llegada, jugador_actual_data, ficha_a_mover_obj, pasos_a_mover
                )
                if movimiento_exitoso:
                    print(f"Ficha {ficha_a_mover_obj['jugador']}-{ficha_a_mover_obj['id']} movida exitosamente.")
                    jugador_actual_data["ultima_ficha_movida"] = ficha_a_mover_obj 

                    if bonus_captura > 0:
                        print(f"¡Bonus de {bonus_captura} pasos por captura!")
                        aplicar_bonus_movimiento(tablero_externo, zonas_llegada, jugador_actual_data, bonus_captura)

                    if bonus_llegada > 0:
                        print(f"¡Bonus de {bonus_llegada} pasos por llegada a la meta!")
                        aplicar_bonus_movimiento(tablero_externo, zonas_llegada, jugador_actual_data, bonus_llegada)

                else:
                    print("No se pudo realizar el movimiento seleccionado.")

        
        jugador_actual_idx = actualizar_turno(jugadores, jugador_actual_idx, dados_son_par)

        
        if all(f["estado"] == "meta" for f in jugador_actual_data["fichas"]):
            print(f"¡Felicidades, {jugador_actual_color.capitalize()} ha ganado el juego!")
            juego_activo = False

        if juego_activo:
            _ = input("\nPresiona Enter para el siguiente turno...") 

if __name__ == "__main__":
    main()