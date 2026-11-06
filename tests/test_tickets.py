

from src.funciones import tickets


RUTA_PRUEBA = "tickets_pruebas_pytest.json"


def preparar_prueba():

    """Usa un archivo separado y guarda el estado original del modulo."""

    ruta_original = tickets.ARCHIVO_TICKETS
    tickets_originales = [ticket.copy() for ticket in tickets.tickets_registrados]

    tickets.ARCHIVO_TICKETS = RUTA_PRUEBA
    tickets.tickets_registrados.clear()

    # El modo w crea o vacia solo el archivo dedicado a estas pruebas.
    with open(RUTA_PRUEBA, "w", encoding="utf-8") as archivo:
        pass

    return ruta_original, tickets_originales


def restaurar_prueba(ruta_original, tickets_originales):

    """Restaura la ruta y los tickets que habia antes del test."""

    tickets.ARCHIVO_TICKETS = ruta_original
    tickets.tickets_registrados[:] = tickets_originales


def test_crear_y_recuperar_ticket():
    ruta, anteriores = preparar_prueba()
    try:
        resultado, id_ticket = tickets.crear_ticket(1, 2, (0, 3), 2500, 1)
        assert resultado is True
        assert id_ticket == 1

        tickets.tickets_registrados.clear()
        resultado, mensaje = tickets.cargar_tickets()
        assert resultado is True
        assert len(tickets.tickets_registrados) == 1
        assert tickets.tickets_registrados[0]["id"] == 1
        assert tickets.tickets_registrados[0]["asiento"] == (0, 3)
    finally:
        restaurar_prueba(ruta, anteriores)


def test_cobrar_ticket():

    ruta, anteriores = preparar_prueba()
    try:
        assert tickets.crear_ticket(1, 2, (0, 3), 2500, 1)[0] is True
        assert tickets.cobrar(1)[0] is True

        tickets.tickets_registrados.clear()
        assert tickets.cargar_tickets()[0] is True
        assert tickets.obtener_ticket(1)["estado"] == "cobrado"
    finally:
        restaurar_prueba(ruta, anteriores)


def test_cancelar_ticket():

    ruta, anteriores = preparar_prueba()
    try:
        assert tickets.crear_ticket(1, 2, (0, 3), 2500, 1)[0] is True
        assert tickets.cancelar_ticket(1)[0] is True

        tickets.tickets_registrados.clear()
        assert tickets.cargar_tickets()[0] is True
        assert tickets.obtener_ticket(1)["estado"] == "cancelado"
    finally:
        restaurar_prueba(ruta, anteriores)


def test_archivo_danado():

    ruta, anteriores = preparar_prueba()
    try:
        assert tickets.crear_ticket(1, 2, (0, 3), 2500, 1)[0] is True
        with open(RUTA_PRUEBA, "w", encoding="utf-8") as archivo:
            archivo.write("datos|incorrectos\n")

        resultado, mensaje = tickets.cargar_tickets()
        assert resultado is False
        assert len(tickets.tickets_registrados) == 1
    finally:
        restaurar_prueba(ruta, anteriores)


def test_error_guardado_al_crear():

    ruta, anteriores = preparar_prueba()
    try:
        # Intentar escribir sobre una carpeta produce un error de archivo.
        tickets.ARCHIVO_TICKETS = "src/datos"
        resultado, mensaje = tickets.crear_ticket(1, 2, (0, 3), 2500, 1)
        assert resultado is False
        assert len(tickets.tickets_registrados) == 0
    finally:
        restaurar_prueba(ruta, anteriores)


def test_error_guardado_al_cobrar():

    ruta, anteriores = preparar_prueba()
    try:
        assert tickets.crear_ticket(1, 2, (0, 3), 2500, 1)[0] is True
        tickets.ARCHIVO_TICKETS = "src/datos"

        resultado, mensaje = tickets.cobrar(1)
        assert resultado is False
        assert tickets.obtener_ticket(1)["estado"] == "pendiente"
    finally:
        restaurar_prueba(ruta, anteriores)


def test_error_guardado_al_cancelar():

    ruta, anteriores = preparar_prueba()
    try:
        assert tickets.crear_ticket(1, 2, (0, 3), 2500, 1)[0] is True
        tickets.ARCHIVO_TICKETS = "src/datos"

        resultado, mensaje = tickets.cancelar_ticket(1)
        assert resultado is False
        assert tickets.obtener_ticket(1)["estado"] == "pendiente"
    finally:
        restaurar_prueba(ruta, anteriores)



def test_recaudacion_recursiva():

    lista = [
        {"estado": "cobrado", "precio": 2500},
        {"estado": "pendiente", "precio": 3000},
        {"estado": "cobrado", "precio": 4000},
        {"estado": "cancelado", "precio": 2000}
    ]

    total = tickets.sumar_recaudacion_recursiva(lista)

    assert total == 6500



def test_recaudacion_lista_vacia():

    total = tickets.sumar_recaudacion_recursiva([])

    assert total == 0


def test_rechaza_asiento_duplicado_y_permite_reutilizar_cancelado():
    ruta, anteriores = preparar_prueba()
    try:
        assert tickets.crear_ticket(1, 2, (0, 0), 2500, 1) == (True, 1)
        assert tickets.crear_ticket(2, 2, (0, 0), 2500, 1)[0] is False
        assert len(tickets.tickets_registrados) == 1
        assert tickets.cancelar_ticket(1)[0] is True
        assert tickets.crear_ticket(2, 2, (0, 0), 2500, 1) == (True, 2)
        assert tickets.crear_ticket(3, 2, (-1, 0), 2500, 1)[0] is False
    finally:
        restaurar_prueba(ruta, anteriores)
