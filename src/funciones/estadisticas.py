
from functools import reduce


def promedio_precio(tickets, estado=None):
    if estado is not None:
        tickets = list(filter(lambda t: t["estado"] == estado, tickets))

    if not tickets:
        return 0

    precios = list(map(lambda t: t["precio"], tickets))
    return sum(precios) / len(precios)


def contar_por_estado(tickets, estado):
    return len(list(filter(lambda t: t["estado"] == estado, tickets)))


def porcentaje_por_estado(tickets, estado):
    if not tickets:
        return 0

    en_estado = list(filter(lambda t: t["estado"] == estado, tickets))
    return len(en_estado) / len(tickets) * 100


def total_recaudado(tickets):
    cobrados = list(filter(lambda t: t["estado"] == "cobrado", tickets))

    if not cobrados:
        return 0

    return reduce(lambda acumulado, t: acumulado + t["precio"], cobrados, 0)


def contar_por_pelicula(tickets, id_pelicula, estado=None):
    """Cuenta los tickets de una película, opcionalmente por estado."""
    return len(list(filter(
        lambda t: t["pelicula_id"] == id_pelicula and (estado is None or t["estado"] == estado),
        tickets
    )))


def resumen_estadisticas(tickets):
    return {
        "promedio_precio": promedio_precio(tickets),
        "cantidad_pendientes": contar_por_estado(tickets, "pendiente"),
        "cantidad_cobrados": contar_por_estado(tickets, "cobrado"),
        "cantidad_cancelados": contar_por_estado(tickets, "cancelado"),
        "porcentaje_cobrados": porcentaje_por_estado(tickets, "cobrado"),
        "total_recaudado": total_recaudado(tickets),
    }



def peliculas_mas_y_menos_vendidas(peliculas, tickets):

    """
    Devuelve la pelicula mas y menos vendida segun tickets cobrados.
    """


    if not peliculas:
        return None, None

    ventas = []

    for pelicula in peliculas:
        cantidad = contar_por_pelicula(tickets, pelicula["id"], "cobrado")
        ventas.append((pelicula["titulo"], cantidad))

    mas_vendida = max(ventas, key=lambda dato: dato[1])
    menos_vendida = min(ventas, key=lambda dato: dato[1])

    return mas_vendida, menos_vendida




def promedio_precio_por_genero(peliculas):

    """
    Calcula el precio promedio de las peliculas por genero.
    """


    totales = {}
    cantidades = {}

    for pelicula in peliculas:
        genero = pelicula["genero"]

        if genero not in totales:
            totales[genero] = 0
            cantidades[genero] = 0

        totales[genero] += pelicula["precio"]
        cantidades[genero] += 1

    promedios = {}

    for genero in totales:
        promedios[genero] = totales[genero] / cantidades[genero]

    return promedios



def clasificar_peliculas_por_ventas(peliculas, tickets):

    """
    Devuelve los IDs de peliculas con ventas y sin ventas.
    """

    ids_catalogo = set()
    ids_vendidos = set()

    # Guardamos todos los IDs del catalogo
    for pelicula in peliculas:
        ids_catalogo.add(pelicula["id"])

    # Guardamos los IDs de peliculas con tickets cobrados
    for ticket in tickets:
        if ticket["estado"] == "cobrado":
            ids_vendidos.add(ticket["pelicula_id"])

    # Interseccion: peliculas existentes con ventas
    con_ventas = ids_catalogo & ids_vendidos

    # Diferencia: peliculas sin ventas
    sin_ventas = ids_catalogo - ids_vendidos

    return con_ventas, sin_ventas




def ranking_peliculas_mas_vendidas(peliculas, tickets, cantidad=3):

    """
    Devuelve las primeras peliculas ordenadas por ventas.
    """


    if cantidad <= 0:
        return []

    ventas = []

    for pelicula in peliculas:
        cobrados = contar_por_pelicula(tickets, pelicula["id"], "cobrado")
        ventas.append((pelicula["titulo"], cobrados))

    # Ordenamos de mayor a menor cantidad de ventas

    ventas.sort(key=lambda dato: dato[1], reverse=True)

    # Devolvemos solo los primeros resultados

    return ventas[:cantidad]


