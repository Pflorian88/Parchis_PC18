NUM_CASILLAS_EXTERNAS = 68
CASILLAS_SEGURAS = [5, 12, 17, 22, 29, 34, 39, 46, 51, 56, 63, 68]
SALIDAS_JUGADORES = {
    "rojo": 5,   
    "verde": 22, 
    "amarillo": 39, 
    "azul": 56    
}
ENTRADAS_LLEGADA = {
    "rojo": 68,   
    "verde": 16, 
    "amarillo": 33, 
    "azul": 50    
}

def inicializar_tablero():

    return [[] for _ in range(NUM_CASILLAS_EXTERNAS)]

def inicializar_zonas_llegada():

    return {
        "rojo": [None] * 8,
        "verde": [None] * 8,
        "amarillo": [None] * 8,
        "azul": [None] * 8
    }

def es_casilla_segura(posicion):

    return posicion in CASILLAS_SEGURAS