"""
CRUD de clientes.
Con JSON y recursividad.
"""

import re
import json
import os
from src.vista import VERDE, imprimir_advertencia, imprimir_error, imprimir_exito, imprimir_mensaje, mostrar_tabla

from src.validaciones import validar_email, validar_telefono

lista_clientes = []
emails_activos = set()
ARCHIVO_CLIENTES = "src/datos/clientes.json"


def guardar_clientes():
    """Guarda la lista de clientes en el archivo JSON."""
    try:
        with open(ARCHIVO_CLIENTES, 'w', encoding="UTF-8") as archivo:
            # ensure_ascii=False para que guarde tildes y ñ correctamente
            json.dump(lista_clientes, archivo, ensure_ascii=False, indent=4)
    except Exception as e:
        imprimir_error(f"No se pudo guardar el archivo de clientes: {e}")


def cargar_clientes_desde_json():
    """Carga los clientes desde el archivo JSON al arrancar el sistema."""
    global lista_clientes, emails_activos
    try:
        with open(ARCHIVO_CLIENTES, 'r', encoding="UTF-8") as archivo:
            lista_clientes = json.load(archivo)
            # Reconstruimos el conjunto de emails para validar duplicados
            emails_activos = {c["email"] for c in lista_clientes}
    except FileNotFoundError:
        # Si el archivo no existe, arranca con listas vacias
        lista_clientes = []
        emails_activos = set()
    except json.JSONDecodeError:
        imprimir_error("El archivo de clientes esta dañado o mal formateado.")
        lista_clientes = []
        emails_activos = set()


def sumar_digitos_telefono_recursivo(telefono):
    """Suma los dígitos de un teléfono de forma recursiva."""
    if len(telefono) == 0:
        return 0
    
    if telefono[0].isdigit():
        return int(telefono[0]) + sumar_digitos_telefono_recursivo(telefono[1:])
    
    return sumar_digitos_telefono_recursivo(telefono[1:])


def contar_clientes_recursivo(clientes, i=0):
    """Cuenta los clientes en la lista de forma recursiva."""
    if i == len(clientes):
        return 0
    return 1 + contar_clientes_recursivo(clientes, i + 1)


def buscar_cliente(id_cliente):
    """Devuelve un cliente por su ID o None si no existe."""
    for cliente in lista_clientes:
        if cliente["id"] == id_cliente:
            return cliente
    return None


def alta_cliente(nombre, email, telefono, mostrar_mensajes=True):
    """Agrega un cliente, lo guarda en JSON y actualiza los conjuntos."""

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
    es_valido_tel, mensaje_tel = validar_telefono(telefono)
    if not es_valido_tel and mostrar_mensajes:
        imprimir_advertencia(mensaje_tel)

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
    
    # Guardamos en el archivo JSON
    guardar_clientes()

    if mostrar_mensajes:
        imprimir_exito(f"Cliente '{nombre}' dado de alta con ID {cliente['id']}")

    return True


def baja_cliente(id_cliente):
    """Realiza la baja logica de un cliente y guarda el cambio en JSON."""
    cliente = buscar_cliente(id_cliente)
    if cliente is None:
        imprimir_error(f"No existe cliente con ID {id_cliente}")
        return False
    if not cliente["estado"]:
        imprimir_advertencia("El cliente ya estaba inactivo")
        return True

    cliente["estado"] = False
    guardar_clientes() # Guardamos en JSON
    imprimir_exito(f"Cliente ID {id_cliente} dado de baja")
    return True


def modificar_cliente(id_cliente, nombre=None, email=None, telefono=None):
    """Modifica los datos de un cliente y guarda el cambio en JSON."""
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

    guardar_clientes() # Guardamos en JSON
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


def obtener_tickets_de_cliente(id_cliente, tickets):
    """Devuelve todos los tickets asociados a un cliente."""
    return list(filter(lambda t: t["cliente_id"] == id_cliente, tickets))


if __name__ == "__main__":
    imprimir_mensaje("=== Prueba del Modulo Clientes ===", VERDE)
    alta_cliente("Lary Choi", "larychoi@email.com", "1122334455")
    alta_cliente("Tomas Moran", "tomasmoran@email.com", "1166778899")
    alta_cliente("Juan Cruz Iocco", "juaniocco@email.com", "1144556677")
    mostrar_clientes()

    # Prueba de recursividad
    print(f"\nSuma de digitos del tel 12345: {sumar_digitos_telefono_recursivo('12345')}")
    print(f"Clientes contados recursivamente: {contar_clientes_recursivo(lista_clientes)}")
    
    print(f"\nSlicing (primeros 1): {listar_clientes_paginado(0, 1)}")
