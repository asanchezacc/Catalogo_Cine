tickets_registrados = []


def obtener_ticket(id_ticket):
    
    """
    Recibe el ID de un ticket.
    Devuelve el ticket encontrado o None si no existe.
    """

    for ticket in tickets_registrados:
        if ticket["id"] == id_ticket:
            return ticket

    return None



def crear_ticket(cliente_id, pelicula_id, asiento, precio, empleado_id):

    """
    Recibe los datos necesarios para crear un ticket.
    Devuelve (True, id_ticket) si pudo crearlo o
    (False, mensaje) si algún dato no es válido.
    """

    if cliente_id <= 0 or pelicula_id <= 0 or empleado_id <= 0:
        return False, "Los identificadores deben ser positivos"

    if precio <= 0:
        return False, "El precio debe ser mayor que cero"

    if type(asiento) != tuple or len(asiento) != 2:
        return False, "El asiento debe ser una tupla de dos elementos"

    id_ticket = len(tickets_registrados) + 1

    nuevo_ticket = {
        "id": id_ticket,
        "cliente_id": cliente_id,
        "pelicula_id": pelicula_id,
        "asiento": asiento,
        "precio": precio,
        "empleado_id": empleado_id,
        "estado": "pendiente"
    }

    tickets_registrados.append(nuevo_ticket)

    return True, id_ticket



def cobrar(id_ticket):

    """
    Recibe el ID de un ticket pendiente.
    Cambia su estado a cobrado.
    Devuelve una tupla indicando el resultado.
    """

    ticket = obtener_ticket(id_ticket)

    if ticket is None:
        return False, "El ticket no existe"

    if ticket["estado"] != "pendiente":
        return False, "El ticket no está pendiente"

    ticket["estado"] = "cobrado"

    return True, "Cobro registrado"



def cancelar_ticket(id_ticket):
    
    """
    Recibe el ID de un ticket pendiente.
    Cambia su estado a cancelado.
    Devuelve una tupla indicando el resultado.
    """

    ticket = obtener_ticket(id_ticket)

    if ticket is None:
        return False, "El ticket no existe"

    if ticket["estado"] != "pendiente":
        return False, "Solo se puede cancelar un ticket pendiente"

    ticket["estado"] = "cancelado"

    return True, "Ticket cancelado"
