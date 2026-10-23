"""
Datos iniciales del sistema.
Carga de clientes, peliculas y usuarios de prueba al arrancar el programa.
"""
import os

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
        if clientes.alta_cliente(nombre, email, telefono, False):
            cantidad += 1
    return cantidad

def cargar_peliculas(lista_peliculas):
    """Da de alta las peliculas de prueba en la lista recibida."""
    cantidad = 0
    id_pelicula = 1

    for datos in PELICULAS_INICIALES:
        titulo, genero, duracion, precio = datos

        if peliculas.agregar_pelicula(lista_peliculas, id_pelicula, titulo, genero, duracion, precio):
            cantidad += 1

        id_pelicula += 1

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
    """Carga todos los datos iniciales y crea la sala, usando JSON si ya existen."""
    imprimir_encabezado("Cargando datos")

    ruta_clientes = "src/datos/clientes.json"
    
    if not os.path.exists(ruta_clientes):
        # Si el archivo no existe, es la primera vez.
        n_clientes = cargar_clientes()
        clientes.guardar_clientes() # Guarda el archivo JSON
        imprimir_mensaje(f"Clientes iniciales creados: {n_clientes}", CYAN)
    else:
        # Si ya existe, los leemos del JSON (no los volvemos a crear).
        clientes.cargar_clientes_desde_json()
        imprimir_mensaje(f"Clientes cargados desde JSON: {len(clientes.lista_clientes)}", CYAN)

    n_peliculas = cargar_peliculas(lista_peliculas)
    imprimir_mensaje(f"Peliculas cargadas: {n_peliculas}", CYAN)

    n_usuarios = cargar_usuarios()
    imprimir_mensaje(f"Usuarios cargados: {n_usuarios}", CYAN)

    sala = asientos.crear_sala(SALA_FILAS, SALA_COLUMNAS)
    imprimir_mensaje(f"Sala creada: {SALA_FILAS}x{SALA_COLUMNAS}", CYAN)

    return sala
