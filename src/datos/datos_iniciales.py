"""
Datos iniciales del sistema.
Carga de clientes, peliculas y usuarios de prueba al arranca el programa.
"""

from src.modelos import clientes, usuarios
from src.funciones import peliculas, asientos
from src.vista import imprimir_mensaje, imprimir_encabezado, CYAN

CLIENTES_INICIALES = [
    ("Lary Choi", "larychoi@email.com", "1122334455"),
    ("Tómas Moran", "tomasmoran@email.com", "1166778899"),
    ("Juan Cruz Iocco", "juaniocco@email.com", "1144556677"),
]

PELICULAS_INICIALES = [
    ("Spiderman Brand New Day", "Accion", 150, 2500),
    ("La Odisea", "Drama", 90, 2000),
    ("Supergirl", "Ciencia ficcion", 120, 2200),
    ("Mortal Kombat II", "Accion", 100, 2400),
    ("Maestros del Universo", "Aventura", 110, 2300),
]

USUARIOS_INICIALES = [
    ("Administrador", "admin", "admin123", "administrador"),
    ("Empleado uno", "empleado1", "1234", "empleado"),
]

SALA_FILAS = 5
SALA_COLUMNAS = 8

def cargar_clientes():
    """Da de alta los clientes de prueba."""
    cantidad = 0
    for nombre, email, telefono in CLIENTES_INICIALES:
        if clientes.alta_cliente(nombre, email, telefono):
            cantidad += 1
    return cantidad

def cargar_peliculas(lista_peliculas):
    """Da de alta las peliculas de prueba en la lista recibida."""
    cantidad = 0
    for id_pelicula, datos in enumerate(PELICULAS_INICIALES, start=1):
        titulo, genero, duracion, precio = datos
        if peliculas.agregar_pelicula(
            lista_peliculas,
            id_pelicula,
            titulo,
            genero,
            duracion,
            precio,
        ):
            cantidad += 1
    return cantidad

def cargar_usuarios():
    """Da de alta los usuarios de prueba"""
    cantidad = 0
    for nombre, usuario, password, rol in USUARIOS_INICIALES:
        ok, _ = usuarios.alta_usuario(nombre, usuario, password, rol)
        if ok:
            cantidad += 1
    return cantidad

def cargar_datos(lista_peliculas):
    """Carga todos los datos iniciales y crea la sala."""
    imprimir_encabezado("Cargando datos")

    n_clientes = cargar_clientes()
    imprimir_mensaje(f"Clientes cargados: {n_clientes}", CYAN)

    n_peliculas = cargar_peliculas(lista_peliculas)
    imprimir_mensaje(f"Peliculas cargadas: {n_peliculas}", CYAN)

    n_usuarios = cargar_usuarios()
    imprimir_mensaje(f"Usuarios cargados: {n_usuarios}", CYAN)

    sala = asientos.crear_sala(SALA_FILAS, SALA_COLUMNAS)
    imprimir_mensaje(f"Sala creada: {SALA_FILAS}x{SALA_COLUMNAS}", CYAN)

    return sala

if __name__ == "__main__":
    lista_peliculas = []
    sala = cargar_datos(lista_peliculas)

    print("\n--- Clientes ---")
    for c in clientes.listar_clientes():
        print(f"ID {c['id']:>2} | {c['nombre']:<20} | {c['email']}")

    print("\n--- Peliculas ---")
    for p in peliculas.listar_peliculas(lista_peliculas):
        print(f"ID {p['id']:>2} | {p['titulo']:<30} | ${p['precio']}")

    print("\n--- Usuarios ---")
    for u in usuarios.usuarios:
        print(f"ID {u['id']:>2} | {u['usuario']:<12} | rol: {u['rol']}")

    print(f"\n--- Sala ({len(sala)} filas x {len(sala[0])} columnas) ---")
    for fila in sala:
        print(" " + "   ".join(str(a) for a in fila))
