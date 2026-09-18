from src.modelos import clientes
from src.funciones import peliculas, asientos, tickets


# ------------------ Clientes ------------------

def alta_cliente(nombre, email, telefono):
    """Da de alta un nuevo cliente. clientes.py ya informa el resultado por pantalla."""
    return clientes.alta_cliente(nombre, email, telefono)


def baja_cliente(id_cliente):
    """Da de baja (lógica) a un cliente por su ID."""
    return clientes.baja_cliente(id_cliente)


def actualizar_cliente(id_cliente, nombre=None, email=None, telefono=None):
    """Modifica los datos (nombre, email y/o teléfono) de un cliente existente."""
    return clientes.modificar_cliente(id_cliente, nombre, email, telefono)


def ver_cliente(id_cliente):
    """Devuelve los datos de un cliente puntual, o None si no existe."""
    return clientes.buscar_cliente(id_cliente)


def listar_clientes(mostrar_inactivos=False):
    """Devuelve la lista de clientes registrados."""
    return clientes.listar_clientes(mostrar_inactivos)


# ------------------ Películas (consulta, sin modificar el catálogo) ------------------

def ver_peliculas(catalogo):
    """Devuelve una copia del catálogo de películas."""
    return peliculas.listar_peliculas(catalogo)


def buscar_pelicula(catalogo, texto):
    """Devuelve las películas cuyo título contiene el texto buscado."""
    return list(filter(lambda p: texto.lower() in p["titulo"].lower(), catalogo))


# ------------------ Sala: matriz -> conjunto -> diccionario ------------------

def asientos_ocupados(sala):
    return {
        (fila_idx, columna_idx)
        for fila_idx, fila in enumerate(sala)
        for columna_idx, estado in enumerate(fila)
        if estado == asientos.ASIENTO_OCUPADO
    }


def mapa_ocupacion(sala):
    """asientos ocupados
    """
    ocupados = asientos_ocupados(sala)
    mapa = {}
    for fila_idx, fila in enumerate(sala):
        for columna_idx in range(len(fila)):
            clave = (fila_idx, columna_idx)
            mapa[clave] = "Ocupado" if clave in ocupados else "Libre"
    return mapa


# ------------------ Reservas y tickets ------------------

def dar_reserva(sala, cliente_id, pelicula_id, precio, fila, columna, empleado_id):
    """
    Ocupa un asiento de la sala y genera el ticket de la reserva.
    """
    if clientes.buscar_cliente(cliente_id) is None:
        return False, "No existe un cliente con ese ID."

    if not asientos.ocupar_asiento(sala, fila, columna):
        return False, "Ese asiento no existe o ya está ocupado."

    asiento = (fila, columna)
    exito, resultado = tickets.crear_ticket(cliente_id, pelicula_id, asiento, precio, empleado_id)

    if not exito:
        asientos.liberar_asiento(sala, fila, columna)
        return False, resultado

    return True, resultado


def cancelar_reserva(sala, id_ticket):
    """
    Cancela un ticket pendiente y libera el asiento que tenía asignado.
    
    """
    ticket = tickets.obtener_ticket(id_ticket)
    if ticket is None:
        return False, "Ese ticket no existe."

    exito, mensaje = tickets.cancelar_ticket(id_ticket)
    if exito:
        fila, columna = ticket["asiento"]
        asientos.liberar_asiento(sala, fila, columna)

    return exito, mensaje


def cobrar_ticket(id_ticket):
    """Cobra un ticket pendiente. Devuelve (True, mensaje) o (False, mensaje)."""
    return tickets.cobrar(id_ticket)


def obtener_datos_ticket(id_ticket, catalogo):
    """
    Junta los datos de un ticket con el título de la película y el
    nombre del cliente.
    """
    ticket = tickets.obtener_ticket(id_ticket)
    if ticket is None:
        return None

    pelicula = peliculas.obtener_pelicula(catalogo, ticket["pelicula_id"])
    cliente = clientes.buscar_cliente(ticket["cliente_id"])

    return {
        "id": ticket["id"],
        "cliente": cliente["nombre"] if cliente else "?",
        "pelicula": pelicula["titulo"] if pelicula else "?",
        "asiento": ticket["asiento"],
        "precio": ticket["precio"],
        "estado": ticket["estado"],
    }


def ver_reservas(empleado_id=None):
    """
    Devuelve los tickets registrados. .
    """
    if empleado_id is None:
        return tickets.tickets_registrados
    return list(filter(lambda t: t["empleado_id"] == empleado_id, tickets.tickets_registrados))