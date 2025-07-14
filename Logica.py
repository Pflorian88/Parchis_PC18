def lanzar_dados():

    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    return dado1, dado2

def crear_fichas(color_jugador, num_fichas=4):

    fichas = []
    for i in range(1, num_fichas + 1):
        fichas.append({
            "jugador": color_jugador,
            "id": i,
            "estado": "carcel",
            "posicion": None
        })
    return fichas

def inicializar_jugadores_data(color, nombre):

    return {
        "nombre": nombre,
        "color": color,
        "fichas": crear_fichas(color),
        "en_juego": 0,
        "pares_consecutivos": 0,
        "ultima_ficha_movida": None
    }

def obtener_movimientos_posibles(jugador_actual_data, tablero_externo, zonas_llegada, dados):

    posibles_movimientos = []
    dado1, dado2 = dados

    if 5 in dados:
        fichas_en_carcel = [f for f in jugador_actual_data["fichas"] if f["estado"] == "carcel"]
        if fichas_en_carcel:

            ficha_a_sacar = fichas_en_carcel[0]
            salida_pos = SALIDAS_JUGADORES[ficha_a_sacar["jugador"]]

            es_bloqueo_salida = False
            if len(tablero_externo[salida_pos]) == 2 and tablero_externo[salida_pos][0]["jugador"] == ficha_a_sacar["jugador"]:
                es_bloqueo_salida = True

            if not es_bloqueo_salida:
                posibles_movimientos.append((ficha_a_sacar, 5))
                return posibles_movimientos

    fichas_en_juego_o_llegada = [f for f in jugador_actual_data["fichas"] if f["estado"] in ["en_juego", "llegada"]]

    for dado_valor in [dado1, dado2]:
        for ficha in fichas_en_juego_o_llegada:
            if validar_movimiento_simulado(tablero_externo, zonas_llegada, ficha, dado_valor):
                if (ficha, dado_valor) not in posibles_movimientos:
                    posibles_movimientos.append((ficha, dado_valor))

    dado_total = dado1 + dado2
    for ficha in fichas_en_juego_o_llegada:
        if validar_movimiento_simulado(tablero_externo, zonas_llegada, ficha, dado_total):
            if (ficha, dado_total) not in posibles_movimientos:
                posibles_movimientos.append((ficha, dado_total))

    return posibles_movimientos

def validar_movimiento_simulado(tablero_externo, zonas_llegada, ficha, pasos):

    if ficha["estado"] == "en_juego":
        pos_actual = ficha["posicion"]

        for i in range(1, pasos + 1):
            siguiente_pos_absoluta = pos_actual + i

            if siguiente_pos_absoluta > NUM_CASILLAS_EXTERNAS -1 and ficha["jugador"] == "rojo": 
                pos_en_llegada = siguiente_pos_absoluta - (NUM_CASILLAS_EXTERNAS)
                if pos_en_llegada >= 8: 
                    return False 
                if zonas_llegada[ficha["jugador"]][pos_en_llegada] is not None:
                     return False
                break

            elif siguiente_pos_absoluta > ENTRADAS_LLEGADA[ficha["jugador"]] and ficha["jugador"] != "rojo":
            
                pass 

            else: 
                pos_intermedia = siguiente_pos_absoluta % NUM_CASILLAS_EXTERNAS
              
                if len(tablero_externo[pos_intermedia]) == 2 and \
                   tablero_externo[pos_intermedia][0]["jugador"] == ficha["jugador"]:
                    return False
        nueva_pos = (pos_actual + pasos) % NUM_CASILLAS_EXTERNAS

        if len(tablero_externo[nueva_pos]) == 2 and \
           tablero_externo[nueva_pos][0]["jugador"] == ficha["jugador"]:
            return False

        return True

    elif ficha["estado"] == "llegada":
        pos_actual = ficha["posicion"]
        nueva_pos_en_llegada = pos_actual + pasos

        if nueva_pos_en_llegada > 7:
            return False
        if zonas_llegada[ficha["jugador"]][nueva_pos_en_llegada] is not None:
            return False 
        return True

    return False