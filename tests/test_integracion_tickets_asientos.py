

from src.funciones import tickets, asientos


RUTA_PRUEBA = "tickets_integracion_pytest.json"


def preparar_prueba():

    ruta_original = tickets.ARCHIVO_TICKETS
    tickets_originales = [ticket.copy() for ticket in tickets.tickets_registrados]

    tickets.ARCHIVO_TICKETS = RUTA_PRUEBA
    tickets.tickets_registrados.clear()

    with open(RUTA_PRUEBA, "w", encoding="utf-8") as archivo:
        pass

    return ruta_original, tickets_originales


def restaurar_prueba(ruta_original, tickets_originales):

    tickets.ARCHIVO_TICKETS = ruta_original
    tickets.tickets_registrados[:] = tickets_originales


def test_reinicio_recupera_asientos():

    ruta, anteriores = preparar_prueba()
    try:
        exito, id_1 = tickets.crear_ticket(1, 2, (0, 0), 2500, 1)
        assert exito is True

        exito, id_2 = tickets.crear_ticket(2, 2, (0, 1), 2500, 1)
        assert exito is True

        exito, id_3 = tickets.crear_ticket(3, 2, (1, 2), 2500, 1)
        assert exito is True

        assert tickets.cobrar(id_2)[0] is True
        assert tickets.cancelar_ticket(id_3)[0] is True

        # Simulacion de reinicio: se pierde lo que estaba en memoria.
        tickets.tickets_registrados.clear()
        sala = asientos.crear_sala(2, 3)

        assert tickets.cargar_tickets()[0] is True
        resultado, mensaje = asientos.reconstruir_ocupacion(
            sala, tickets.tickets_registrados
        )
        assert resultado is True
        assert asientos.obtener_estado_asiento(sala, 0, 0) == asientos.ASIENTO_OCUPADO
        assert asientos.obtener_estado_asiento(sala, 0, 1) == asientos.ASIENTO_OCUPADO
        assert asientos.obtener_estado_asiento(sala, 1, 2) == asientos.ASIENTO_LIBRE
        assert asientos.contar_asientos_libres(sala) == 4
    finally:
        restaurar_prueba(ruta, anteriores)


def test_reinicio_detecta_duplicados():
    
    ruta, anteriores = preparar_prueba()
    try:
        assert tickets.crear_ticket(1, 2, (0, 0), 2500, 1)[0] is True
        # Simulamos un archivo manipulado con dos reservas del mismo asiento.
        ticket_duplicado = tickets.obtener_ticket(1).copy()
        ticket_duplicado["id"] = 2
        tickets.tickets_registrados.append(ticket_duplicado)
        assert tickets.guardar_tickets()[0] is True

        tickets.tickets_registrados.clear()
        sala = asientos.crear_sala(2, 3)
        sala_anterior = [fila[:] for fila in sala]

        assert tickets.cargar_tickets()[0] is True
        resultado, mensaje = asientos.reconstruir_ocupacion(
            sala, tickets.tickets_registrados
        )
        assert resultado is False
        assert sala == sala_anterior
    finally:
        restaurar_prueba(ruta, anteriores)
