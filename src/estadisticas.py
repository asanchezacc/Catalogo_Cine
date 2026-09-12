from functools import reduce


def promedio_precio(reservas, estado=None):
    if estado is not None:
        reservas = list(filter(lambda fila: fila[5] == estado, reservas))

    if not reservas:
        return 0

    precios = list(map(lambda fila: fila[4], reservas))
    return sum(precios) / len(precios)


def contar_por_estado(reservas, estado):
    return len(list(filter(lambda fila: fila[5] == estado, reservas)))


def contar_por_empleado(reservas, empleado):
    return len(list(filter(lambda fila: fila[3] == empleado, reservas)))


def porcentaje_por_estado(reservas, estado):
    if not reservas:
        return 0

    en_estado = list(filter(lambda fila: fila[5] == estado, reservas))
    return len(en_estado) / len(reservas) * 100


def total_recaudado(reservas):
    cobradas = list(filter(lambda fila: fila[5] == "cobrada", reservas))

    if not cobradas:
        return 0

    return reduce(lambda acumulado, fila: acumulado + fila[4], cobradas, 0)


def porcentaje_clientes(usuarios):
    pares = list(usuarios.items())

    if not pares:
        return 0

    clientes = list(filter(lambda par: par[1]["rol"] == "cliente", pares))
    return len(clientes) / len(pares) * 100


def resumen_estadisticas(reservas):
    return {
        "promedio_precio": promedio_precio(reservas),
        "cantidad_pendientes": contar_por_estado(reservas, "pendiente"),
        "cantidad_cobradas": contar_por_estado(reservas, "cobrada"),
        "porcentaje_cobradas": porcentaje_por_estado(reservas, "cobrada"),
        "total_recaudado": total_recaudado(reservas),
    }


if __name__ == "__main__":
    prueba = [
        [1, "cliente1", "Película 1", "empleado1", 1500, "cobrada"],
        [2, "cliente2", "Película 2", "empleado1", 1800, "pendiente"],
        [3, "cliente1", "Película 3", "empleado1", 1200, "cobrada"],
    ]

    print(promedio_precio(prueba))
    print(promedio_precio(prueba, estado="cobrada"))
    print(contar_por_estado(prueba, "pendiente"))
    print(contar_por_empleado(prueba, "empleado1"))
    print(porcentaje_por_estado(prueba, "cobrada"))
    print(total_recaudado(prueba))
    print(resumen_estadisticas(prueba))

    usuarios_prueba = {
        "admin": {"contrasena": "x", "rol": "administrador"},
        "empleado1": {"contrasena": "x", "rol": "empleado"},
        "cliente1": {"contrasena": "x", "rol": "cliente"},
        "cliente2": {"contrasena": "x", "rol": "cliente"},
    }
    print(porcentaje_clientes(usuarios_prueba))
