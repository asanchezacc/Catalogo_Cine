from .asientos import ocupar_asiento, liberar_asiento


def obtener_ticket(tickets, id_ticket):

    """
    recibe una lista de diccionarios y el ID buscado.
    devuelve el ticket encontrado o None si no existe.
    """
      
    for ticket in tickets:
        if ticket["id"] == id_ticket:
            return ticket

    return None


def crear_ticket(tickets, sala, id_ticket, cliente_id,
                 pelicula_id, fila, columna, precio):

    """
    recibe la lista de tickets, la sala correspondiente,
    IDs enteros y un precio numérico.
    El cliente y la película deben existir previamente.
    registra el ticket y ocupa el asiento.
    Devuelve True si pudo crearlo o False si no pudo.
    """
       
    if id_ticket <= 0 or cliente_id <= 0 or pelicula_id <= 0:
        return False

    if precio <= 0:
        return False

    if obtener_ticket(tickets, id_ticket) is not None:
        return False

    if not ocupar_asiento(sala, fila, columna):
        return False

    nuevo_ticket = {
        "id": id_ticket,
        "cliente_id": cliente_id,
        "pelicula_id": pelicula_id,
        "asiento": (fila, columna),
        "precio": precio,
        "estado": "activo"
    }

    tickets.append(nuevo_ticket)

    return True


def cancelar_ticket(tickets, sala, id_ticket):

    """
    recibe la lista de tickets, la sala correspondiente
    al ticket y el ID que se desea cancelar.
    libera el asiento y marca el ticket como cancelado.
    Devuelve True si pudo cancelarlo o False si no pudo.
    """

    ticket = obtener_ticket(tickets, id_ticket)

    if ticket is None:
        return False

    if ticket["estado"] != "activo":
        return False

    fila, columna = ticket["asiento"]

    if not liberar_asiento(sala, fila, columna):
        return False

    ticket["estado"] = "cancelado"

    return True