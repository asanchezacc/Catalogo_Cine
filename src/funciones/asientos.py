ASIENTO_LIBRE = 0
ASIENTO_OCUPADO = 1



def crear_sala(filas, columnas):
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
    if len(sala) == 0:
        return False

    if fila < 0 or fila >= len(sala):
        return False

    if columna < 0 or columna >= len(sala[fila]):
        return False

    return True



def obtener_estado_asiento(sala, fila, columna):
    if not asiento_valido(sala, fila, columna):
        return None

    return sala[fila][columna]



def ocupar_asiento(sala, fila, columna):
    if not asiento_valido(sala, fila, columna):
        return False

    if sala[fila][columna] == ASIENTO_OCUPADO:
        return False

    sala[fila][columna] = ASIENTO_OCUPADO
    return True



def liberar_asiento(sala, fila, columna):
    if not asiento_valido(sala, fila, columna):
        return False

    if sala[fila][columna] == ASIENTO_LIBRE:
        return False

    sala[fila][columna] = ASIENTO_LIBRE
    return True



def contar_asientos_libres(sala):
    cantidad = 0

    for fila in sala:
        for asiento in fila:
            if asiento == ASIENTO_LIBRE:
                cantidad = cantidad + 1

    return cantidad


