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

    
    ultimo_id = 0

    for ticket in tickets_registrados:
        if ticket["id"] > ultimo_id:
            ultimo_id = ticket["id"]

    id_ticket = ultimo_id + 1


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

    guardado, mensaje = guardar_tickets()

    if not guardado:
        tickets_registrados.pop()
        return False, mensaje

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

    guardado, mensaje = guardar_tickets()

    if not guardado:
        ticket["estado"] = "pendiente"
        return False, mensaje

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

    guardado, mensaje = guardar_tickets()

    if not guardado:
        ticket["estado"] = "pendiente"
        return False, mensaje

    return True, "Ticket cancelado"




ARCHIVO_TICKETS = "src/datos/tickets.txt"


def guardar_tickets():

    """Guarda los tickets en un archivo de texto."""

    try:
        with open(ARCHIVO_TICKETS, "w", encoding="utf-8") as archivo:
            for ticket in tickets_registrados:
                fila, columna = ticket["asiento"]

                campos = [
                    ticket["id"],
                    ticket["cliente_id"],
                    ticket["pelicula_id"],
                    fila,
                    columna,
                    ticket["precio"],
                    ticket["empleado_id"],
                    ticket["estado"]
                ]

                linea = "|".join(str(campo) for campo in campos)
                archivo.write(linea + "\n")

        return True, "Tickets guardados correctamente"

    except OSError as error:
        return False, f"No se pudieron guardar los tickets: {error}"


def cargar_tickets():

    """Recupera los tickets guardados en el archivo de texto."""

    cargados = []

    try:
        with open(ARCHIVO_TICKETS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split("|")

                if len(partes) != 8:
                    raise ValueError("Formato de ticket inválido")

                id_ticket, id_cliente, id_pelicula, fila, columna, precio, empleado, estado = partes

                if estado not in ("pendiente", "cobrado", "cancelado"):
                    raise ValueError("Estado de ticket inválido")

                cargados.append({
                    "id": int(id_ticket),
                    "cliente_id": int(id_cliente),
                    "pelicula_id": int(id_pelicula),
                    "asiento": (int(fila), int(columna)),
                    "precio": float(precio),
                    "empleado_id": int(empleado),
                    "estado": estado
                })

    except FileNotFoundError:
        return True, "Todavía no existe un archivo de tickets"

    except (OSError, ValueError) as error:
        return False, f"No se pudieron cargar los tickets: {error}"

    tickets_registrados[:] = cargados
    return True, f"Se cargaron {len(cargados)} tickets"


