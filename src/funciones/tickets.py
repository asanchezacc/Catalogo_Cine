
import json


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

    if (type(cliente_id) != int or type(pelicula_id) != int
            or type(empleado_id) != int or cliente_id <= 0
            or pelicula_id <= 0 or empleado_id <= 0):
        return False, "Los identificadores deben ser enteros positivos"

    if type(precio) not in (int, float) or precio <= 0:
        return False, "El precio debe ser mayor que cero"

    if type(asiento) != tuple or len(asiento) != 2:
        return False, "El asiento debe ser una tupla de dos elementos"
    fila, columna = asiento
    if (type(fila) != int or type(columna) != int
            or fila < 0 or columna < 0):
        return False, "Las coordenadas del asiento no son válidas"

    for ticket in tickets_registrados:
        if ticket["estado"] != "cancelado" and ticket["asiento"] == asiento:
            return False, "El asiento ya está reservado en otro ticket"

    
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





ARCHIVO_TICKETS = "src/datos/tickets.json"


def guardar_tickets():


    """
    Guarda los tickets en un archivo JSON.
    """


    try:
        with open(ARCHIVO_TICKETS, "w", encoding="utf-8") as archivo:
            json.dump(tickets_registrados, archivo, ensure_ascii=False, indent=4)

        return True, "Tickets guardados correctamente"

    except (OSError, TypeError, ValueError) as error:
        return False, f"No se pudieron guardar los tickets: {error}"


def cargar_tickets():


    """
    Recupera tickets desde JSON y transforma los asientos en tuplas.
    """


    cargados = []
    ids = set()

    try:
        with open(ARCHIVO_TICKETS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if type(datos) != list:
            raise ValueError("El archivo debe contener una lista de tickets")

        for ticket in datos:
            if type(ticket) != dict:
                raise ValueError("Un ticket tiene un formato incorrecto")

            for clave in ("id", "cliente_id", "pelicula_id", "asiento", "precio", "empleado_id", "estado"):
                if clave not in ticket:
                    raise ValueError(f"Falta el campo {clave} en un ticket")

            if type(ticket["id"]) != int or ticket["id"] <= 0 or ticket["id"] in ids:
                raise ValueError("ID de ticket invalido o repetido")

            ids.add(ticket["id"])

            for campo in ("cliente_id", "pelicula_id", "empleado_id"):
                if type(ticket[campo]) != int or ticket[campo] <= 0:
                    raise ValueError(f"El campo {campo} no es valido")

            if type(ticket["precio"]) not in (int, float) or ticket["precio"] <= 0:
                raise ValueError("Precio de ticket invalido")

            asiento = ticket["asiento"]

            if type(asiento) != list or len(asiento) != 2:
                raise ValueError("Asiento de ticket invalido")

            fila, columna = asiento

            if type(fila) != int or type(columna) != int or fila < 0 or columna < 0:
                raise ValueError("Coordenadas de asiento invalidas")

            if ticket["estado"] not in ("pendiente", "cobrado", "cancelado"):
                raise ValueError("Estado de ticket invalido")

            ticket_cargado = ticket.copy()
            ticket_cargado["asiento"] = (fila, columna)

            cargados.append(ticket_cargado)

    except FileNotFoundError:
        tickets_registrados.clear()
        return True, "Todavia no existe un archivo de tickets"

    except (OSError, ValueError, TypeError) as error:
        return False, f"No se pudieron cargar los tickets: {error}"

    tickets_registrados[:] = cargados

    return True, f"Se cargaron {len(cargados)} tickets"




def sumar_recaudacion_recursiva(lista_tickets, indice=0):


    """
    Calcula recursivamente el total de tickets cobrados.
    """

    # Caso base: llegamos al final de la lista
    if indice >= len(lista_tickets):
        return 0

    ticket = lista_tickets[indice]

    # Si esta cobrado, sumamos su precio
    if ticket["estado"] == "cobrado":
        return ticket["precio"] + sumar_recaudacion_recursiva(
            lista_tickets, indice + 1
        )

    # Si no esta cobrado, seguimos sin sumarlo
    return sumar_recaudacion_recursiva(lista_tickets, indice + 1)
