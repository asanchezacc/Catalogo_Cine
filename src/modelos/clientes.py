"""
CRUD de clientes
Funciones para validar emails, evitar duplicados, ordenar con lambda, vista para mensajes y tablas
"""
import re
from src.vista import (imprimir_error, imprimir_exito, imprimir_advertencia, mostrar_tabla, imprimir_mensaje, VERDE, RESET)

clientes = [] # lista de diccionarios
emails_activos = set() # conjunto de emails
id_counter = 1

def validar_email(email):
    """Valida formato de email con expresión regular."""
    patron = r'^[a-zA-z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_telefono(telefono):
    """Valida que el telefono contenga solo digitos"""
    return telefono.isdigit()

def buscar_cliente(id_cliente):
    """Devuelve el diccionario del cliente o None si no existe."""
    for cli in clientes:
        if cli["id"] == id_cliente:
            return cli
    return None

def alta_cliente(nombre, email, telefono):
    """Da de alta a un nuevo cliente"""
    global id_counter
    if not nombre.strip():
        imprimir_error("El nombre no puede estar vacio")
        return False
    if not validar_email(email):
        imprimir_error("Formato de email invalido")
        return False
    if email in emails_activos:
        imprimir_error("Este email ya esta registrado")
        return False
    if not validar_telefono(telefono):
        imprimir_advertencia("El telefono debe contener solo digitos")
    cliente = {
        "id": id_counter,
        "nombre": nombre.strip(),
        "email": email,
        "telefono": telefono,
        "estado": True
    }
    clientes.append(cliente)
    emails_activos.add(email)
    id_counter += 1
    imprimir_exito(f"Cliente '{nombre}' dado de alta con ID {cliente['id']}")
    return True

def baja_cliente(id_cliente):
    """Realiza baja logica"""
    cliente = buscar_cliente(id_cliente)
    if not cliente:
        imprimir_error(f"No existe cliente con ID {id_cliente}")
        return False
    if not cliente["estado"]:
        imprimir_advertencia("El cliente ya estaba inactivo")
        return True
    cliente["estado"] = False
    # No removemos el email del conjunto para mantener historial
    imprimir_exito(f"Cliente ID {id_cliente} dado de baja")
    return True

def modificar_cliente(id_cliente, nombre=None, email=None, telefono=None):
    """Modifica los datos de un cliente existente."""
    cliente = buscar_cliente(id_cliente)
    if not cliente:
        imprimir_error(f"No existe cliente con ID {id_cliente}")
        return False

    # Validar email si se proporciona
    if email is not None:
        if not validar_email(email):
            imprimir_error("Formato de email invalido.")
            return False
        # Si el email cambio, verificar que no este en uso por otro cliente
        if email != cliente["email"] and email in emails_activos:
            imprimir_error("El email ya esta registrado por otro cliente")
            return False
        # Actualizar conjunto
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
    """Retorna una lista de clientes"""
    if mostrar_inactivos:
        return clientes.copy()
    return [cli for cli in clientes if cli["estado"]]

def mostrar_clientes(mostrar_inactivos=False):
    """Muestra la tabla de clientes"""
    datos = listar_clientes(mostrar_inactivos)
    if not datos:
        imprimir_advertencia("No hay clientes para mostrar")
        return

    #Convertir estado a texto para mostrar
    for fila in datos:
        fila["estado"] = "Activo" if fila["estado"] else "Inactivo"

    columnas = [
        ("ID", "id", 5),
        ("Nombre", "nombre", 25),
        ("Email", "email", 30),
        ("Telefono", "telefono", 15),
        ("Estado", "estado", 10)
    ]
    mostrar_tabla(datos, columnas)

def ordenar_clientes(campo, reverse=False):
    """Ordena la lista de clientes usando lambda"""
    if campo not in ("id", "nombre", "email", "estado"):
        imprimir_error("Campo invalido para ordenar")
        return clientes.copy()
    # Convertir estado a booleno para ordenar correctamente
    if campo == "estado":
        return sorted(clientes, key=lambda cli: cli["estado"], reverse=reverse)
    return sorted(clientes, key=lambda cli: cli[campo], reverse=reverse)

def clientes_activos_conjunto():
    """Retorna un conjunto de IDs de clientes activos"""
    return {cli["id"] for cli in clientes if cli["estado"]}

if __name__ == "__main__":
    imprimir_mensaje("=== Prueba del Módulo Clientes ===", VERDE)

    # Alta de clientes
    alta_cliente("Lary Choi", "larychoi@email.com", "1122334455")
    alta_cliente("Tómas Moran", "tomasmoran@email.com", "1166778899")
    alta_cliente("Juan Cruz Iocco", "juaniocco@email.com", "1144556677")

    print("\n--- Clientes Activos ---")
    mostrar_clientes()

    print("\n--- Ordenados por Nombre ---")
    ordenados = ordenar_clientes("nombre")
    for cli in ordenados:
        print(f"{cli['id']}: {cli['nombre']} - {cli['email']}")

    print("\n--- Modificando Cliente ID 1 ---")
    modificar_cliente(1, email="lary.choi@email.com")

    print("\n--- Baja Cliente ID 2 ---")
    baja_cliente(2)

    print("\n--- Clientes ---")
    mostrar_clientes(mostrar_inactivos=True)

    print("\n--- Conjunto de IDs Activos ---")
    print(clientes_activos_conjunto())
