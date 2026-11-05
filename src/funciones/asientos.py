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

    if obtener_estado_asiento(sala, fila, columna) != ASIENTO_LIBRE:
        return False

    sala[fila][columna] = ASIENTO_OCUPADO
    return True



def liberar_asiento(sala, fila, columna):

    """
    Recibe una sala con estados 0 y 1 y los índices de un asiento.
    Libera el asiento si está ocupado y devuelve True.
    Si es inválido o ya está libre, devuelve False sin modificarlo.
    """

    if obtener_estado_asiento(sala, fila, columna) != ASIENTO_OCUPADO:
        return False

    sala[fila][columna] = ASIENTO_LIBRE
    return True




def contar_asientos_libres(sala, fila=0, columna=0):


    """
    Cuenta recursivamente los asientos libres de una sala.
    Recorre las columnas y avanza por las filas.
    """


    # Caso base: terminamos de recorrer toda la sala

    if fila >= len(sala):
        return 0

    # Si terminamos una fila, pasamos a la siguiente

    if columna >= len(sala[fila]):
        return contar_asientos_libres(sala, fila + 1, 0)

    # Comprobamos si el asiento actual esta libre

    cantidad = 0

    if sala[fila][columna] == ASIENTO_LIBRE:
        cantidad = 1

    # Sumamos el asiento actual y seguimos recorriendo

    return cantidad + contar_asientos_libres(
        sala, fila, columna + 1
    )




def reconstruir_ocupacion(sala, lista_tickets):


    """
    Reconstruye los asientos ocupados usando los tickets.
    Los tickets pendientes y cobrados ocupan asientos.
    Los tickets cancelados no ocupan asientos.
    """


    nueva_sala = []

    for fila in sala:
        nueva_sala.append([ASIENTO_LIBRE] * len(fila))

    for ticket in lista_tickets:
        estado = ticket["estado"]

        if estado not in ("pendiente", "cobrado", "cancelado"):
            return False, "Estado de ticket invalido"

        if estado != "cancelado":
            fila, columna = ticket["asiento"]

            if not ocupar_asiento(nueva_sala, fila, columna):
                return False, "Asiento invalido o duplicado"

    # Actualizamos la sala solo si todo fue correcto
    sala[:] = nueva_sala

    return True, "Ocupacion recuperada correctamente"

