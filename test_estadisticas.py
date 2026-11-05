


from src.funciones import estadisticas


PELICULAS = [
    {"id": 1, "titulo": "Accion A", "genero": "Accion", "precio": 2000},
    {"id": 2, "titulo": "Drama B", "genero": "Drama", "precio": 3000},
    {"id": 3, "titulo": "Accion C", "genero": "Accion", "precio": 4000},
]


def test_pelicula_mas_y_menos_vendida():

    tickets = [
        {"pelicula_id": 1, "estado": "cobrado"},
        {"pelicula_id": 1, "estado": "cobrado"},
        {"pelicula_id": 2, "estado": "cobrado"},
        {"pelicula_id": 3, "estado": "pendiente"},
        {"pelicula_id": 3, "estado": "cancelado"},
    ]

    mas, menos = estadisticas.peliculas_mas_y_menos_vendidas(
        PELICULAS, tickets
    )

    assert mas == ("Accion A", 2)
    assert menos == ("Accion C", 0)


def test_no_contar_tickets_pendientes():

    tickets = [{"pelicula_id": 2, "estado": "pendiente"}]

    mas, menos = estadisticas.peliculas_mas_y_menos_vendidas(
        PELICULAS, tickets
    )

    assert mas[1] == 0
    assert menos[1] == 0


def test_promedio_por_genero():

    promedios = estadisticas.promedio_precio_por_genero(PELICULAS)

    assert promedios == {"Accion": 3000, "Drama": 3000}


def test_sin_peliculas():

    assert estadisticas.peliculas_mas_y_menos_vendidas([], []) == (None, None)
    assert estadisticas.promedio_precio_por_genero([]) == {}



def test_clasificar_peliculas_conjuntos():

    tickets = [
        {"pelicula_id": 1, "estado": "cobrado"},
        {"pelicula_id": 2, "estado": "cobrado"},
        {"pelicula_id": 3, "estado": "cancelado"},
        {"pelicula_id": 99, "estado": "cobrado"}
    ]

    con_ventas, sin_ventas = estadisticas.clasificar_peliculas_por_ventas(
        PELICULAS, tickets
    )

    assert con_ventas == {1, 2}
    assert sin_ventas == {3}


def test_ranking_peliculas_slicing():

    tickets = [
        {"pelicula_id": 1, "estado": "cobrado"},
        {"pelicula_id": 1, "estado": "cobrado"},
        {"pelicula_id": 2, "estado": "cobrado"},
        {"pelicula_id": 3, "estado": "cancelado"}
    ]

    ranking = estadisticas.ranking_peliculas_mas_vendidas(
        PELICULAS, tickets, 2
    )

    assert ranking == [("Accion A", 2), ("Drama B", 1)]


def test_ranking_cantidad_invalida():

    resultado = estadisticas.ranking_peliculas_mas_vendidas(
        PELICULAS, [], 0
    )

    assert resultado == []



def test_contar_por_pelicula_y_estado():
    tickets = [
        {"pelicula_id": 1, "estado": "cobrado"},
        {"pelicula_id": 1, "estado": "cancelado"},
        {"pelicula_id": 2, "estado": "cobrado"},
    ]
    assert estadisticas.contar_por_pelicula(tickets, 1) == 2
    assert estadisticas.contar_por_pelicula(tickets, 1, "cobrado") == 1
    assert estadisticas.contar_por_pelicula(tickets, 1, "pendiente") == 0
