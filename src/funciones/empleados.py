"""importar las demas funciones cuando esten echas"""

def borrar_cliente(id_cliente):
    """Da de baja a un cliente."""
    return clientes.eliminar_cliente(id_cliente)


def ver_cliente(id_cliente):
    """Muestra los datos de un cliente."""
    return clientes.obtener_cliente(id_cliente)


def lista_clientes():
    """Muestra todos los clientes."""
    return clientes.lista_clientes()


# ------------------ Reservas, asientos y tickets ------------------

def dar_asiento(id_asiento, id_cliente, id_pelicula, precio):
    """Ocupa un asiento y genera el ticket de la reserva."""
    ok, resultado = asientos.ocupar_asiento(id_asiento)
    if not ok:
        return False, resultado
    return tickets.crear_ticket(id_cliente, id_pelicula, id_asiento, precio)


def cancelar_reserva(id_ticket):
    """Cancela un ticket y libera el asiento que tenía asignado."""
    ticket = tickets.obtener_ticket(id_ticket)
    if ticket is None:
        return False, "Ticket no encontrado."

    asientos.liberar_asiento(ticket["asiento_id"])
    return tickets.cancelar_ticket(id_ticket)


def cobrar(id_ticket):
    """Cobra un ticket ya generado."""
    ticket = tickets.obtener_ticket(id_ticket)
    if ticket is None:
        return False, "Ticket no encontrado."
    return True, f"Cobrado ${ticket['precio']} del ticket {id_ticket}."


def imprimir_ticket(id_ticket):
    """Imprime los datos de un ticket."""
    ticket = tickets.obtener_ticket(id_ticket)
    if ticket is None:
        return False, "Ticket no encontrado."
    print(f"--- Ticket #{ticket['id']} ---")
    print(f"Cliente: {ticket['cliente_id']}")
    print(f"Película: {ticket['pelicula_id']}")
    print(f"Asiento: {ticket['asiento_id']}")
    print(f"Precio: ${ticket['precio']}")
    return True, "Ticket impreso."


def ver_reservas():
    """Muestra todas las reservas hechas."""
    return tickets.listar_tickets()


# ------------------ Consultas al catálogo de películas ------------------

def ver_peliculas():
    """Muestra el catálogo completo de películas."""
    return peliculas.listar_peliculas()


def buscar_pelicula(nombre):
    """Busca película en especifico"""
    todas = peliculas.listar_peliculas()
    return list(filter(lambda p: nombre.lower() in p["nombre"].lower(), todas))