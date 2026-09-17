"""CRUD de clientes."""

import re

from src.vista import (
    VERDE,
    imprimir_advertencia,
    imprimir_error,
    imprimir_exito,
    imprimir_mensaje,
    mostrar_tabla,
)


lista_clientes = []
emails_activos = set()
id_counter = 1


def validar_email(email):
    """Valida el formato de un email."""
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email) is not None


def validar_telefono(telefono):
    """Valida que el telefono contenga solo digitos."""
    return telefono.isdigit()


def buscar_cliente(id_cliente):
    """Devuelve un cliente por su ID o None si no existe."""
    for cliente in lista_clientes:
        if cliente["id"] == id_cliente:
            return cliente
    return None


def alta_cliente(nombre, email, telefono, mostrar_mensajes=True):
    """Agrega un cliente si sus datos basicos son validos."""
    global id_counter

    if not nombre.strip():
        if mostrar_mensajes:
            imprimir_error("El nombre no puede estar vacio")
        return False
    if not validar_email(email):
        if mostrar_mensajes:
            imprimir_error("Formato de email invalido")
        return False
    if email in emails_activos:
        if mostrar_mensajes:
            imprimir_error("Este email ya esta registrado")
        return False

    if not validar_telefono(telefono) and mostrar_mensajes:
        imprimir_advertencia("El telefono debe contener solo digitos")

    cliente = {
        "id": id_counter,
        "nombre": nombre.strip(),
        "email": email,
        "telefono": telefono,
        "estado": True,
    }
    lista_clientes.append(cliente)
    emails_activos.add(email)
    id_counter += 1

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
        if not validar_email(email):
            imprimir_error("Formato de email invalido.")
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
        if not validar_telefono(telefono):
            imprimir_advertencia("El telefono debe contener solo digitos")
        cliente["telefono"] = telefono

    imprimir_exito(f"Cliente ID {id_cliente} modificado correctamente")
    return True


def listar_clientes(mostrar_inactivos=False):
    """Devuelve copias de los clientes activos o de todos los clientes."""
    if mostrar_inactivos:
        return [cliente.copy() for cliente in lista_clientes]
    return [cliente.copy() for cliente in lista_clientes if cliente["estado"]]


def mostrar_clientes(mostrar_inactivos=False):
    """Muestra los clientes en formato de tabla."""
    datos = listar_clientes(mostrar_inactivos)
    if not datos:
        imprimir_advertencia("No hay clientes para mostrar")
        return

    datos_mostrar = [
        {**cliente, "estado": "Activo" if cliente["estado"] else "Inactivo"}
        for cliente in datos
    ]
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
    return {cliente["id"] for cliente in lista_clientes if cliente["estado"]}


if __name__ == "__main__":
    imprimir_mensaje("=== Prueba del Modulo Clientes ===", VERDE)
    alta_cliente("Lary Choi", "larychoi@email.com", "1122334455")
    alta_cliente("Tomas Moran", "tomasmoran@email.com", "1166778899")
    alta_cliente("Juan Cruz Iocco", "juaniocco@email.com", "1144556677")
    mostrar_clientes()
