"""
CRUD de clientes.
Con JSON y recursividad.
"""

import json
from src.vista import VERDE, imprimir_advertencia, imprimir_error, imprimir_exito, imprimir_mensaje, mostrar_tabla

from src.validaciones import validar_email, validar_telefono

lista_clientes = []
emails_activos = set()
ARCHIVO_CLIENTES = "src/datos/clientes.json"


def guardar_clientes():
    """Guarda la lista de clientes en JSON y devuelve True si pudo hacerlo."""
    try:
        with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as archivo:
            json.dump(lista_clientes, archivo, ensure_ascii=False, indent=4)
        return True
    except (OSError, TypeError, ValueError) as error:
        imprimir_error(f"No se pudo guardar el archivo de clientes: {error}")
        return False


def cargar_clientes_desde_json():
    """Devuelve True si carga, None si no existe y False si hay errores."""
    cargados = []
    ids = set()
    emails = set()

    try:
        with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if type(datos) != list:
            raise ValueError("El archivo debe contener una lista de clientes.")

        for cliente in datos:
            if type(cliente) != dict:
                raise ValueError("Hay un cliente con un formato incorrecto.")

            for campo in ("id", "nombre", "email", "telefono", "estado"):
                if campo not in cliente:
                    raise ValueError(f"Falta el campo {campo} en un cliente.")

            id_cliente = cliente["id"]
            email = cliente["email"]
            if type(email) != str:
                raise ValueError("Hay un email con un formato incorrecto.")
            email_normalizado = email.strip().lower()
            if type(id_cliente) != int or id_cliente <= 0 or id_cliente in ids:
                raise ValueError("Hay un ID de cliente inválido o repetido.")
            if type(cliente["nombre"]) != str or not cliente["nombre"].strip():
                raise ValueError("Hay un nombre de cliente inválido.")
            if email_normalizado in emails or not validar_email(email_normalizado)[0]:
                raise ValueError("Hay un email inválido o repetido.")
            if type(cliente["telefono"]) != str or type(cliente["estado"]) != bool:
                raise ValueError("Hay datos de un cliente con un formato incorrecto.")

            cargados.append(cliente)
            ids.add(id_cliente)
            emails.add(email_normalizado)

    except FileNotFoundError:
        lista_clientes.clear()
        emails_activos.clear()
        return None
    except (OSError, ValueError, TypeError, UnicodeError) as error:
        imprimir_error(f"No se pudo cargar el archivo de clientes: {error}")
        return False

    lista_clientes[:] = cargados
    emails_activos.clear()
    emails_activos.update(emails)
    return True


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

    # Normalizar el email para detectar duplicados con distintas mayúsculas.
    if type(email) != str:
        if mostrar_mensajes:
            imprimir_error("El email debe ser texto")
        return False
    email = email.strip().lower()
    es_valido, mensaje = validar_email(email)
    if not es_valido:
        if mostrar_mensajes:
            imprimir_error(mensaje)
        return False
    
    if email in emails_activos:
        if mostrar_mensajes:
            imprimir_error("Este email ya esta registrado")
        return False

    # El teléfono debe ser válido antes de registrar al cliente.
    es_valido_tel, mensaje_tel = validar_telefono(telefono)
    if not es_valido_tel:
        if mostrar_mensajes:
            imprimir_error(mensaje_tel)
        return False

    nuevo_id = 1
    for registrado in lista_clientes:
        if registrado["id"] >= nuevo_id:
            nuevo_id = registrado["id"] + 1

    cliente = {
        "id": nuevo_id,
        "nombre": nombre.strip(),
        "email": email,
        "telefono": telefono,
        "estado": True,
    }

    lista_clientes.append(cliente)
    emails_activos.add(email)

    if not guardar_clientes():
        lista_clientes.pop()
        emails_activos.remove(email)
        return False

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
    if not guardar_clientes():
        cliente["estado"] = True
        return False
    imprimir_exito(f"Cliente ID {id_cliente} dado de baja")
    return True


def modificar_cliente(id_cliente, nombre=None, email=None, telefono=None):
    """Valida antes de modificar y revierte los cambios si falla el guardado."""
    cliente = buscar_cliente(id_cliente)
    if cliente is None:
        imprimir_error(f"No existe cliente con ID {id_cliente}")
        return False

    if email is not None:
        if type(email) != str:
            imprimir_error("El email debe ser texto")
            return False
        email = email.strip().lower()
        es_valido, mensaje = validar_email(email)
        if not es_valido:
            imprimir_error(mensaje)
            return False
        email_anterior = cliente["email"].strip().lower()
        if email != email_anterior and email in emails_activos:
            imprimir_error("El email ya esta registrado por otro cliente")
            return False

    if nombre is not None and not nombre.strip():
        imprimir_error("El nombre no puede estar vacio")
        return False

    if telefono is not None:
        es_valido, mensaje = validar_telefono(telefono)
        if not es_valido:
            imprimir_error(mensaje)
            return False

    datos_anteriores = cliente.copy()
    emails_anteriores = emails_activos.copy()

    if email is not None:
        email_anterior = cliente["email"].strip().lower()
        if email != email_anterior:
            emails_activos.remove(email_anterior)
            emails_activos.add(email)
        cliente["email"] = email
    if nombre is not None:
        cliente["nombre"] = nombre.strip()
    if telefono is not None:
        cliente["telefono"] = telefono

    if not guardar_clientes():
        cliente.clear()
        cliente.update(datos_anteriores)
        emails_activos.clear()
        emails_activos.update(emails_anteriores)
        return False

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
