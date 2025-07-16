def mostrar_tablero(tablero_externo, zonas_llegada, jugadores):

    print("\n--- Estado del Tablero ---")

  
    print("\nTablero Externo:")

    num_columnas = 4
    num_filas = (len(tablero_externo) + num_columnas - 1) // num_columnas

    for fila in range(num_filas):
        linea = ""
        for col in range(num_columnas):
            idx = fila + col * num_filas
            if idx < len(tablero_externo):
                fichas_en_casilla = ", ".join([f"{f['jugador'][0].upper()}{f['id']}" for f in tablero_externo[idx]])
                linea += f"Casilla {idx}: [{fichas_en_casilla}]" .ljust(35)
        print(linea)

    print("\nZonas de Llegada:")
    for color, zona in zonas_llegada.items():
        fichas_en_zona = ", ".join([f"{f['jugador'][0].upper()}{f['id']}" if f else "-" for f in zona])
        print(f"{color.capitalize()}: [{fichas_en_zona}]")

    print("\nCárceles:")
    for color, jugador_data in jugadores.items():
        fichas_en_carcel = [f"{f['jugador'][0].upper()}{f['id']}" for f in jugador_data["fichas"] if f["estado"] == "carcel"]
        print(f"{color.capitalize()}: [{', '.join(fichas_en_carcel)}]")

def pedir_opcion_movimiento(movimientos_posibles):

    if not movimientos_posibles:
        print("No hay movimientos válidos.")
        return None, 0

    print("\nMovimientos posibles:")
    for i, (ficha, pasos) in enumerate(movimientos_posibles):
        print(f"  {i+1}. Mover ficha {ficha['jugador']}-{ficha['id']} ({ficha['estado']}, Pos: {ficha['posicion']}) {pasos} pasos.")

    while True:
        try:
            seleccion = input("Selecciona el número del movimiento a realizar (o 'c' para cancelar): ").strip().lower()
            if seleccion == 'c':
                return None, 0
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(movimientos_posibles):
                return movimientos_posibles[seleccion - 1]
            else:
                print("Número inválido. Intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número o 'c'.")