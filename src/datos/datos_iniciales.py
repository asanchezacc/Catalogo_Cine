"""
Datos iniciales del sistema.
Carga de clientes, peliculas y usuarios de prueba al arrancar el programa.
"""
from src.modelos import clientes, usuarios
from src.funciones import peliculas

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
        if clientes.alta_cliente(nombre, email, telefono, False):
            cantidad += 1
    return cantidad

def cargar_peliculas(lista_peliculas):
    """Da de alta las peliculas de prueba en la lista recibida."""
    estado = peliculas.cargar_peliculas_desde_json(lista_peliculas)
    if estado is True:
        return len(lista_peliculas)
    if estado is False:
        return None

    lista_peliculas.clear()
    cantidad = 0
    id_pelicula = 1

    for datos in PELICULAS_INICIALES:
        titulo, genero, duracion, precio = datos

        if not peliculas.agregar_pelicula(
            lista_peliculas,
            id_pelicula,
            titulo,
            genero,
            duracion,
            precio,
        ):
            return None
        cantidad += 1
        id_pelicula += 1

    return cantidad

def cargar_usuarios():
    """Da de alta los usuarios de prueba"""
    cantidad = 0
    for nombre, usuario, password, rol in USUARIOS_INICIALES:
        ok, _ = usuarios.alta_usuario(nombre, usuario, password, rol, persistir=False)
        if ok:
            cantidad += 1
    return cantidad

def inicializar_usuarios():
    """Recupera los usuarios del TXT o crea los predeterminados la primera vez."""
    exito, existe_archivo, mensaje = usuarios.cargar_usuarios_desde_txt()
    if not exito:
        return False, mensaje

    if existe_archivo:
        return True, mensaje

    usuarios.usuarios.clear()
    cargar_usuarios()
    return usuarios.guardar_usuarios()
