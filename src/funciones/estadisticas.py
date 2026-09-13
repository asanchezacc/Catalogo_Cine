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


def contar_por_pelicula(tickets, id_pelicula):
    return len(list(filter(lambda t: t["pelicula_id"] == id_pelicula, tickets)))


def resumen_estadisticas(tickets):
    return {
        "promedio_precio": promedio_precio(tickets),
        "cantidad_pendientes": contar_por_estado(tickets, "pendiente"),
        "cantidad_cobrados": contar_por_estado(tickets, "cobrado"),
        "cantidad_cancelados": contar_por_estado(tickets, "cancelado"),
        "porcentaje_cobrados": porcentaje_por_estado(tickets, "cobrado"),
        "total_recaudado": total_recaudado(tickets),
    }
