ASIENTO_LIBRE = 0
ASIENTO_OCUPADO = 1



def crear_sala(filas, columnas):

    """
    Recibe cantidades enteras de filas y columnas.
    Devuelve una matriz nueva con todos los asientos libres.
    Si alguna dimensión no es positiva, devuelve una lista vacía.
    """

    if filas <= 0 or columnas <= 0:
        return []
    
    sala = []

    for i in range(filas):
        fila = []

        for j in range(columnas):
            fila.append(ASIENTO_LIBRE)

        sala.append(fila)

    return sala



def asiento_valido(sala, fila, columna):

    """
    Recibe una sala y los índices enteros de fila y columna.
    Devuelve True si las coordenadas existen o False si no existen.
    Los índices comienzan en cero.
    """
        
    if len(sala) == 0:
        return False

    if fila < 0 or fila >= len(sala):
        return False

    if columna < 0 or columna >= len(sala[fila]):
        return False

    return True



def obtener_estado_asiento(sala, fila, columna):

    """
    Recibe una sala y los índices de un asiento.
    Devuelve 0 si está libre, 1 si está ocupado
    o None si las coordenadas son inválidas.
    """

    if not asiento_valido(sala, fila, columna):
        return None

    return sala[fila][columna]



def ocupar_asiento(sala, fila, columna):

    """
    Recibe una sala con estados 0 y 1 y los índices de un asiento.
    Ocupa el asiento si está libre y devuelve True.
    Si es inválido o ya está ocupado, devuelve False sin modificarlo.
    """

    if not asiento_valido(sala, fila, columna):
        return False

    if sala[fila][columna] == ASIENTO_OCUPADO:
        return False

    sala[fila][columna] = ASIENTO_OCUPADO
    return True



def liberar_asiento(sala, fila, columna):

    """
    Recibe una sala con estados 0 y 1 y los índices de un asiento.
    Libera el asiento si está ocupado y devuelve True.
    Si es inválido o ya está libre, devuelve False sin modificarlo.
    """

    if not asiento_valido(sala, fila, columna):
        return False

    if sala[fila][columna] == ASIENTO_LIBRE:
        return False

    sala[fila][columna] = ASIENTO_LIBRE
    return True



def contar_asientos_libres(sala):

    """
    Recibe una matriz de asientos con estados 0 y 1.
    Devuelve la cantidad de asientos cuyo estado es libre.
    No modifica la sala.
    """

    cantidad = 0

    for fila in sala:
        for asiento in fila:
            if asiento == ASIENTO_LIBRE:
                cantidad = cantidad + 1

    return cantidad


