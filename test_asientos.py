

from src.funciones import asientos


def test_sala_inicial():
    sala = asientos.crear_sala(2, 3)
    assert asientos.contar_asientos_libres(sala) == 6


def test_ocupar_asiento():
    sala = asientos.crear_sala(2, 3)
    assert asientos.ocupar_asiento(sala, 0, 1) is True
    assert asientos.contar_asientos_libres(sala) == 5


def test_liberar_asiento():
    sala = asientos.crear_sala(2, 3)
    assert asientos.ocupar_asiento(sala, 0, 1) is True
    assert asientos.liberar_asiento(sala, 0, 1) is True
    assert asientos.contar_asientos_libres(sala) == 6


def test_sala_vacia():
    assert asientos.contar_asientos_libres([]) == 0


def test_recuperar_asientos():
    sala = asientos.crear_sala(2, 3)
    lista_tickets = [
        {"id": 1, "asiento": (0, 1), "estado": "pendiente"},
        {"id": 2, "asiento": (1, 2), "estado": "cobrado"},
        {"id": 3, "asiento": (0, 2), "estado": "cancelado"},
    ]

    resultado, mensaje = asientos.reconstruir_ocupacion(sala, lista_tickets)
    assert resultado is True
    assert asientos.contar_asientos_libres(sala) == 4
    assert asientos.obtener_estado_asiento(sala, 0, 2) == asientos.ASIENTO_LIBRE


def test_asientos_duplicados():
    sala = asientos.crear_sala(2, 3)
    lista_tickets = [
        {"id": 1, "asiento": (0, 1), "estado": "pendiente"},
        {"id": 2, "asiento": (0, 1), "estado": "cobrado"},
    ]
    sala_original = [fila[:] for fila in sala]

    resultado, mensaje = asientos.reconstruir_ocupacion(sala, lista_tickets)
    assert resultado is False
    assert sala == sala_original


def test_asiento_fuera_de_rango():
    sala = asientos.crear_sala(2, 3)
    lista_tickets = [
        {"id": 1, "asiento": (5, 0), "estado": "pendiente"},
    ]
    sala_original = [fila[:] for fila in sala]

    resultado, mensaje = asientos.reconstruir_ocupacion(sala, lista_tickets)
    assert resultado is False
    assert sala == sala_original
