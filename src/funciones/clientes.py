"""
CRUD de clientes
Funciones para agregar, leer, actualizar y eliminar clientes
"""

def agregar_cliente(clientes, id_cliente, nombre, email, telefono, estado=True):
    """Agrega un nuevo cliente si el ID no existe."""
    # Verificar si el ID ya existe
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return False

    # Crear diccionario con el cliente
    nuevo_cliente = {
        "id": id_cliente,
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "estado": estado
    }

    clientes.append(nuevo_cliente)
    return True

def obtener_cliente(clientes, id_cliente):
    """Obtiene un cliente por su ID, devuelve None si no existe."""
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return cliente
    return None

def listar_clientes(clientes):
    """Devuelve una copia de la lista completa de clientes."""
    return clientes[:]

def actualizar_cliente(clientes, id_cliente, nombre=None, email=None, telefono=None, estado=None):
    """Actualiza los campos de un cliente existente."""
    cliente = obtener_cliente(clientes, id_cliente)

    if cliente is None:
        return False

    # Actulizar solo los campos no None
    if nombre is not None:
        cliente["Nombre"] = nombre
    if email is not None:
        cliente["email"] = email
    if telefono is not None:
        cliente["telefono"] = telefono
    if estado is not None:
        cliente["estado"] = estado

    return True

def eliminar_cliente(clientes, id_cliente):
    """Elimina un cliente del listado por su ID."""
    for i, cliente in enumerate(clientes):
        if cliente["id"] == id_cliente:
            clientes.pop(i)
            return True
    return False

def contar_clientes(clientes):
    """Retorna el total de clientes registrados."""
    return len(clientes)

def listar_clientes_activos(clientes):
    """Devuelve solo los clientes con estado activo"""
    return list(filter(lambda c: c["estado"], clientes))

def contar_clientes_activos(clientes):
    """Cuenta cuantos clientes tienen estado activo."""
    return len(listar_clientes_activos(clientes))

# BLOQUE DE EJECUCION
if __name__ == "__main__":
    # Datos de prueba
    clientes = [
        {"id": 1, "nombre": "Lary Choi", "email": "larychoi@mail.com", "telefono": "1122334455", "estado": True},
        {"id": 2, "nombre": "Tómas Moran", "email": "tomasmoran@mail.com", "telefono": "1166778899", "estado": False},
    ]

    print("--- LISTA INICIAL ---")
    for c in listar_clientes(clientes):
        print(f"ID: {c['id']} | {c['nombre']} | {c['email']} | Activo: {c['estado']}")

    print("\n--- AGREGANDO CLIENTE ---")
    resultado = agregar_cliente(clientes, 3, "Juan Cruz Iocco", "juancruziocco@email.com", "1133557799")
    print("Agregado" if resultado else "No se pudo agregar")

    print("\n--- ACTUALIZANDO CLIENTE ID 2 ---")
    actualizar_cliente(clientes, 2, estado=True)
    print(obtener_cliente(clientes, 2))

    print("\n--- CLIENTES ACTIVOS ---")
    for c in listar_clientes_activos(clientes):
        print(f"ID: {c['id']} | {c['nombre']}")

    print(f"\nTotal de clientes: {contar_clientes(clientes)}")
    print(f"Total de clientes activos: {contar_clientes_activos(clientes)}")

    print("\n--- ELIMINANDO CLIENTE ID 1 ---")
    eliminar_cliente(clientes, 1)
    for c in listar_clientes(clientes):
        print(f"ID: {c['id']} | {c['nombre']}")
