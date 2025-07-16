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

def mover_ficha(tablero_externo, zonas_llegada, jugador_actual_data, ficha, pasos):

    bonus_captura = 0
    bonus_llegada = 0

    if ficha["estado"] == "carcel":
        if pasos == 5:
            salida_pos = SALIDAS_JUGADORES[ficha["jugador"]]

            if len(tablero_externo[salida_pos]) == 2 and tablero_externo[salida_pos][0]["jugador"] == ficha["jugador"]:
                print(f"La casilla de salida para {ficha['jugador']} está bloqueada por fichas propias.")
                return False, 0, 0 

            ficha_en_salida_ajena = None
            if len(tablero_externo[salida_pos]) == 1 and tablero_externo[salida_pos][0]["jugador"] != ficha["jugador"]:
                ficha_en_salida_ajena = tablero_externo[salida_pos].pop(0) 
                capturar_ficha(ficha_en_salida_ajena)
                bonus_captura = 20
                print(f"¡{ficha['jugador']}-{ficha['id']} capturó a {ficha_en_salida_ajena['jugador']}-{ficha_en_salida_ajena['id']} al salir!")

            ficha["estado"] = "en_juego"
            ficha["posicion"] = salida_pos
            tablero_externo[salida_pos].append(ficha)
            jugador_actual_data["en_juego"] += 1
            print(f"Ficha {ficha['jugador']}-{ficha['id']} salió de la cárcel a la casilla {salida_pos}.")
            return True, bonus_captura, bonus_llegada
        else:
            print("Solo puedes sacar una ficha de la cárcel con un 5.")
            return False, 0, 0

    elif ficha["estado"] == "en_juego":
        pos_actual = ficha["posicion"]

        for i in range(1, pasos + 1):
            interim_pos = (pos_actual + i) % NUM_CASILLAS_EXTERNAS
            if len(tablero_externo[interim_pos]) == 2 and tablero_externo[interim_pos][0]["jugador"] == ficha["jugador"]:
                print(f"Movimiento bloqueado en la casilla {interim_pos} por fichas propias.")
                return False, 0, 0 

        nueva_pos = (pos_actual + pasos) % NUM_CASILLAS_EXTERNAS

        cruzando_entrada = False
        if ficha["jugador"] == "rojo" and pos_actual < ENTRADAS_LLEGADA["rojo"] and (pos_actual + pasos) >= ENTRADAS_LLEGADA["rojo"]:
            cruzando_entrada = True
        elif ficha["jugador"] == "verde" and pos_actual < ENTRADAS_LLEGADA["verde"] and (pos_actual + pasos) >= ENTRADAS_LLEGADA["verde"]:
            cruzando_entrada = True
        elif ficha["jugador"] == "amarillo" and pos_actual < ENTRADAS_LLEGADA["amarillo"] and (pos_actual + pasos) >= ENTRADAS_LLEGADA["amarillo"]:
            cruzando_entrada = True
        elif ficha["jugador"] == "azul" and pos_actual < ENTRADAS_LLEGADA["azul"] and (pos_actual + pasos) >= ENTRADAS_LLEGADA["azul"]:
            cruzando_entrada = True

        if cruzando_entrada:

            pasos_restantes = (pos_actual + pasos) - ENTRADAS_LLEGADA[ficha["jugador"]]
            pos_en_llegada = pasos_restantes

            if pos_en_llegada < 8: 
                tablero_externo[pos_actual].remove(ficha)

                if zonas_llegada[ficha["jugador"]][pos_en_llegada] is not None:
                    print(f"La casilla {pos_en_llegada} en la zona de llegada de {ficha['jugador']} está ocupada.")
                    tablero_externo[pos_actual].append(ficha)
                    return False, 0, 0

                ficha["estado"] = "llegada"
                ficha["posicion"] = pos_en_llegada
                zonas_llegada[ficha["jugador"]][pos_en_llegada] = ficha
                print(f"¡{ficha['jugador']}-{ficha['id']} ha entrado a su zona de llegada en la posición {pos_en_llegada}!")

                if pos_en_llegada == 7:
                    ficha["estado"] = "meta"
                    ficha["posicion"] = None
                    zonas_llegada[ficha["jugador"]][7] = None 
                    jugador_actual_data["en_juego"] -= 1 
                    bonus_llegada = 10
                    print(f"¡{ficha['jugador']}-{ficha['id']} ha llegado a la meta!")

                return True, bonus_captura, bonus_llegada 

            else:
                print(f"El movimiento excedería la zona de llegada. Necesitas un movimiento exacto para llegar a la meta.")
                return False, 0, 0 
        tablero_externo[pos_actual].remove(ficha)

        if len(tablero_externo[nueva_pos]) == 2 and tablero_externo[nueva_pos][0]["jugador"] == ficha["jugador"]:
            print(f"La casilla de destino {nueva_pos} está bloqueada por dos fichas de {ficha['jugador']}.")
            tablero_externo[pos_actual].append(ficha) 
            return False, 0, 0

        tablero_externo[nueva_pos].append(ficha)
        ficha["posicion"] = nueva_pos

        if len(tablero_externo[nueva_pos]) == 2 and \
           tablero_externo[nueva_pos][0]["jugador"] != ficha["jugador"] and \
           not es_casilla_segura(nueva_pos):

            ficha_capturada = None
            for f in tablero_externo[nueva_pos]:
                if f != ficha: 
                    ficha_capturada = f
                    break

            if ficha_capturada:
                tablero_externo[nueva_pos].remove(ficha_capturada) 
                capturar_ficha(ficha_capturada)
                bonus_captura = 20
                print(f"¡{ficha['jugador']}-{ficha['id']} capturó a {ficha_capturada['jugador']}-{ficha_capturada['id']} en la casilla {nueva_pos}!")

        return True, bonus_captura, bonus_llegada 

    elif ficha["estado"] == "llegada":
        pos_actual = ficha["posicion"]
        nueva_pos_en_llegada = pos_actual + pasos

        if nueva_pos_en_llegada == 7: 
            zonas_llegada[ficha["jugador"]][pos_actual] = None 
            ficha["estado"] = "meta"
            ficha["posicion"] = None
            jugador_actual_data["en_juego"] -= 1 
            bonus_llegada = 10
            print(f"¡{ficha['jugador']}-{ficha['id']} ha llegado a la meta!")
            return True, bonus_captura, bonus_llegada
        elif nueva_pos_en_llegada < 7:
            if zonas_llegada[ficha["jugador"]][nueva_pos_en_llegada] is not None:
                print(f"La casilla {nueva_pos_en_llegada} en la zona de llegada de {ficha['jugador']} está ocupada.")
                return False, 0, 0 

            zonas_llegada[ficha["jugador"]][pos_actual] = None 
            ficha["posicion"] = nueva_pos_en_llegada
            zonas_llegada[ficha["jugador"]][nueva_pos_en_llegada] = ficha 
            print(f"¡{ficha['jugador']}-{ficha['id']} se movió a la casilla {nueva_pos_en_llegada} en la zona de llegada!")
            return True, bonus_captura, bonus_llegada
        else:
            print(f"Necesitas un movimiento exacto para la meta. Con {pasos} te pasas.")
            return False, 0, 0

    return False, 0, 0 
def capturar_ficha(ficha_capturada):

    ficha_capturada["estado"] = "carcel"
    ficha_capturada["posicion"] = None

def aplicar_bonus_movimiento(tablero_externo, zonas_llegada, jugador_actual_data, pasos_bonus):

    print(f"¡Aplicando bonus de {pasos_bonus} pasos!")
    opciones_bonus = [f for f in jugador_actual_data["fichas"] if f["estado"] in ["en_juego", "llegada"]]

    if not opciones_bonus:
        print("No hay fichas para mover con el bonus.")
        return False

    if len(opciones_bonus) == 1:
        ficha_elegida = opciones_bonus[0]
        print(f"Movimiento automático de {ficha_elegida['jugador']}-{ficha_elegida['id']} con el bonus.")
    else:
        print("Elige una ficha para mover con el bonus:")
        for i, ficha in enumerate(opciones_bonus):
            print(f"  {i+1}. {ficha['jugador']}-{ficha['id']} (Estado: {ficha['estado']}, Pos: {ficha['posicion']})")

        while True:
            try:
                seleccion = int(input("Selecciona el número de la ficha: "))
                if 1 <= seleccion <= len(opciones_bonus):
                    ficha_elegida = opciones_bonus[seleccion - 1]
                    break
                else:
                    print("Número inválido. Intenta de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número.")

    movimiento_exitoso, _, _ = mover_ficha(tablero_externo, zonas_llegada, jugador_actual_data, ficha_elegida, pasos_bonus)
    if movimiento_exitoso:
        print(f"Ficha {ficha_elegida['jugador']}-{ficha_elegida['id']} movida {pasos_bonus} pasos de bonus.")
    else:
        print(f"No se pudo mover la ficha {ficha_elegida['jugador']}-{ficha_elegida['id']} con el bonus.")

    return movimiento_exitoso
def actualizar_turno(jugadores, jugador_actual_idx, dados_son_par):

    jugador_actual_color = list(jugadores.keys())[jugador_actual_idx]

    if dados_son_par:
        jugadores[jugador_actual_color]["pares_consecutivos"] += 1
        print("¡Par! Repites turno.")
        return jugador_actual_idx 
    else:
        jugadores[jugador_actual_color]["pares_consecutivos"] = 0
        return (jugador_actual_idx + 1) % len(jugadores)


