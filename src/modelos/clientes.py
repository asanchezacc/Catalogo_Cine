"""CRUD de clientes."""

import re

from src.vista import VERDE, imprimir_advertencia, imprimir_error, imprimir_exito, imprimir_mensaje, mostrar_tabla

from src.validaciones import validar_email, validar_telefono

lista_clientes = []
emails_activos = set()


def buscar_cliente(id_cliente):
    """Devuelve un cliente por su ID o None si no existe."""
    for cliente in lista_clientes:
        if cliente["id"] == id_cliente:
            return cliente
    return None


def alta_cliente(nombre, email, telefono, mostrar_mensajes=True):
    """Agrega un cliente si sus datos basicos son validos."""

    if not nombre.strip():
        if mostrar_mensajes:
            imprimir_error("El nombre no puede estar vacio")
        return False

    """Validaciones de email usando el modulo centralizado"""
    es_valido, mensaje = validar_email(email)
    if not es_valido:
        if mostrar_mensajes:
            imprimir_error(mensaje)
        return False
    
    if email in emails_activos:
        if mostrar_mensajes:
            imprimir_error("Este email ya esta registrado")
        return False

    """Validacion de telefono: si es que falla, se advierte pero no se rechaza"""
    es_valido, mensaje = validar_telefono(telefono)
    if not es_valido and mostrar_mensajes:
        imprimir_advertencia(mensaje)

    nuevo_id = len(lista_clientes) + 1

    cliente = {
        "id": nuevo_id,
        "nombre": nombre.strip(),
        "email": email,
        "telefono": telefono,
        "estado": True,
    }

    lista_clientes.append(cliente)
    emails_activos.add(email)

    if mostrar_mensajes:
        imprimir_exito(f"Cliente '{nombre}' dado de alta con ID {cliente['id']}")

    return True


def baja_cliente(id_cliente):
    """Realiza la baja logica de un cliente."""
    cliente = buscar_cliente(id_cliente)
    if cliente is None:
        imprimir_error(f"No existe cliente con ID {id_cliente}")
        return False
    if not cliente["estado"]:
        imprimir_advertencia("El cliente ya estaba inactivo")
        return True

    cliente["estado"] = False
    imprimir_exito(f"Cliente ID {id_cliente} dado de baja")
    return True


def modificar_cliente(id_cliente, nombre=None, email=None, telefono=None):
    """Modifica los datos recibidos de un cliente existente."""
    cliente = buscar_cliente(id_cliente)
    if cliente is None:
        imprimir_error(f"No existe cliente con ID {id_cliente}")
        return False

    if email is not None:
        es_valido, mensaje = validar_email(email)
        if not es_valido:
            imprimir_error(mensaje)
            return False
        if email != cliente["email"] and email in emails_activos:
            imprimir_error("El email ya esta registrado por otro cliente")
            return False
        if email != cliente["email"]:
            emails_activos.remove(cliente["email"])
            emails_activos.add(email)
        cliente["email"] = email

    if nombre is not None:
        if not nombre.strip():
            imprimir_error("El nombre no puede estar vacio")
            return False
        cliente["nombre"] = nombre.strip()

    if telefono is not None:
        es_valido, mensaje = validar_telefono(telefono)
        if not es_valido:
            imprimir_advertencia(mensaje)
        cliente["telefono"] = telefono

    imprimir_exito(f"Cliente ID {id_cliente} modificado correctamente")
    return True


def listar_clientes(mostrar_inactivos=False):
    """Devuelve copias de los clientes activos o de todos los clientes."""
    if mostrar_inactivos:
        return [cliente.copy() for cliente in lista_clientes]
    return [cliente.copy() for cliente in lista_clientes if cliente["estado"]]


def listar_clientes_paginado(inicio=0, fin=None):
    """Devuelve una porcion de la lista de clientes usando slicing."""
    if fin is None:
        return lista_clientes[inicio:]
    return lista_clientes[inicio:fin]


def mostrar_clientes(mostrar_inactivos=False):
    """Muestra los clientes en formato de tabla."""
    datos = listar_clientes(mostrar_inactivos)
    if not datos:
        imprimir_advertencia("No hay clientes para mostrar")
        return

    datos_mostrar = []

    for cliente in datos:
        cliente_mostrar = cliente.copy()

        if cliente["estado"]:
            cliente_mostrar["estado"] = "Activo"
        else:
            cliente_mostrar["estado"] = "Inactivo"

        datos_mostrar.append(cliente_mostrar)


    columnas = [
        ("ID", "id", 5),
        ("Nombre", "nombre", 25),
        ("Email", "email", 30),
        ("Telefono", "telefono", 15),
        ("Estado", "estado", 10),
    ]
    mostrar_tabla(datos_mostrar, columnas)


def ordenar_clientes(campo, reverse=False):
    """Devuelve los clientes ordenados por un campo permitido."""
    if campo not in ("id", "nombre", "email", "estado"):
        imprimir_error("Campo invalido para ordenar")
        return [cliente.copy() for cliente in lista_clientes]
    return sorted(lista_clientes, key=lambda cliente: cliente[campo], reverse=reverse)


def clientes_activos_conjunto():
    """Devuelve un conjunto con los IDs de clientes activos."""

    ids_activos = set()

    for cliente in lista_clientes:
        if cliente["estado"]:
            ids_activos.add(cliente["id"])

    return ids_activos


def obtener_tickets_de_clientes(id_cliente, tickets):
    """Devuelve todos los tickets asociados a un cliente."""
    return list(filter(lambda t: t["cliente_id"] == id_cliente, tickets))


if __name__ == "__main__":
    imprimir_mensaje("=== Prueba del Modulo Clientes ===", VERDE)
    alta_cliente("Lary Choi", "larychoi@email.com", "1122334455")
    alta_cliente("Tomas Moran", "tomasmoran@email.com", "1166778899")
    alta_cliente("Juan Cruz Iocco", "juaniocco@email.com", "1144556677")
    mostrar_clientes()
