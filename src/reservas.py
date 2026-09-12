RESERVAS = []


def _proximo_id(reservas):
    if not reservas:
        return 1
    ids = [fila[0] for fila in reservas]
    return max(ids) + 1


def buscar_reserva(id_reserva, reservas):
    for fila in reservas:
        if fila[0] == id_reserva:
            return fila
    return None


def crear_reserva(cliente, pelicula, empleado, precio, reservas):
    id_reserva = _proximo_id(reservas)
    reservas.append([id_reserva, cliente, pelicula, empleado, precio, "pendiente"])
    return id_reserva, f"Reserva #{id_reserva} creada."


def cobrar_reserva(id_reserva, reservas, empleado=None):
    reserva = buscar_reserva(id_reserva, reservas)

    if reserva is None:
        return False, "Esa reserva no existe."

    if reserva[5] == "cobrada":
        return False, "Esa reserva ya estaba cobrada."

    if reserva[3] is None and empleado is not None:
        reserva[3] = empleado

    reserva[5] = "cobrada"
    return True, f"Reserva #{id_reserva} cobrada (${reserva[4]})."


def imprimir_ticket(id_reserva, reservas):
    reserva = buscar_reserva(id_reserva, reservas)

    if reserva is None:
        return False, "Esa reserva no existe."

    if reserva[5] != "cobrada":
        return False, "Todavía no se cobró esta reserva."

    _, cliente, pelicula, empleado, precio, estado = reserva

    lineas = [
        f"{'TICKET':-^30}",
        f"Reserva:  #{id_reserva}",
        f"Película: {pelicula}",
        f"Cliente:  {cliente}",
        f"Atendió:  {empleado}",
        f"Precio:   ${precio}",
        "-" * 30,
    ]

    ticket = "\n".join(lineas)
    return True, ticket


def ver_reservas(reservas, empleado=None, cliente=None):
    resultado = reservas

    if empleado is not None:
        resultado = list(filter(lambda fila: fila[3] == empleado, resultado))

    if cliente is not None:
        resultado = list(filter(lambda fila: fila[1] == cliente, resultado))

    return resultado


def ordenar_reservas_por_precio(reservas, descendente=False):
    return sorted(reservas, key=lambda fila: fila[4], reverse=descendente)


def clientes_con_reservas(reservas):
    return set([fila[1] for fila in reservas])


if __name__ == "__main__":
    prueba = []

    id1, msg1 = crear_reserva("cliente1", "Película 1", "empleado1", 1500, prueba)
    print(msg1)

    print(cobrar_reserva(id1, prueba))
    print(cobrar_reserva(id1, prueba))

    exito, ticket = imprimir_ticket(id1, prueba)
    print(ticket)

    id2, _ = crear_reserva("cliente2", "Película 2", "empleado1", 1800, prueba)
    id3, _ = crear_reserva("cliente1", "Película 3", "empleado1", 1200, prueba)

    print(ver_reservas(prueba, empleado="empleado1"))
    print(ver_reservas(prueba, cliente="cliente1"))
    print(ordenar_reservas_por_precio(prueba, descendente=True))
    print(clientes_con_reservas(prueba))

    id4, _ = crear_reserva("cliente2", "Película 1", None, 1500, prueba)
    print(cobrar_reserva(id4, prueba, empleado="empleado1"))
    print(buscar_reserva(id4, prueba))
