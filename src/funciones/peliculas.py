"""
CRUD de películas
Funciones para agregar, leer, actualizar y eliminar películas
"""

import json


ARCHIVO_PELICULAS = "src/datos/peliculas.json"


def guardar_peliculas(peliculas):
    """Guarda el catálogo de películas en un archivo JSON."""
    try:
        with open(ARCHIVO_PELICULAS, "w", encoding="UTF-8") as archivo:
            json.dump(peliculas, archivo, ensure_ascii=False, indent=4)
    except (OSError, TypeError, json.JSONDecodeError):
        return False
    return True


def cargar_peliculas_desde_json(peliculas):
    """Carga el catálogo de películas desde un archivo JSON."""
    try:
        with open(ARCHIVO_PELICULAS, "r", encoding="UTF-8") as archivo:
            datos = json.load(archivo)
        if type(datos) != list:
            return False
        peliculas.clear()
        peliculas.extend(datos)
    except (FileNotFoundError, OSError, json.JSONDecodeError, TypeError):
        return False
    return True

def agregar_pelicula(peliculas, id_pelicula, titulo, genero, duracion, precio):
    """Agrega una nueva película al catálogo si el ID no existe."""
    # Verificar si el ID ya existe
    for pelicula in peliculas:
        if pelicula["id"] == id_pelicula:
            return False

    titulo = titulo.strip()
    if len(titulo) > 50:
        titulo = titulo[:47] + "..."
    
    # Crear diccionario con la película
    nueva_pelicula = {
        "id": id_pelicula,
        "titulo": titulo,
        "genero": genero,
        "duracion": duracion,
        "precio": precio
    }
    
    peliculas.append(nueva_pelicula)
    if not guardar_peliculas(peliculas):
        peliculas.pop()
        return False
    return True


def obtener_pelicula(peliculas, id_pelicula):
    """Obtiene una película por su ID, devuelve None si no existe."""
    for pelicula in peliculas:
        if pelicula["id"] == id_pelicula:
            return pelicula
    return None


def listar_peliculas(peliculas):
    """Devuelve una copia de la lista completa de películas."""
    return [pelicula.copy() for pelicula in peliculas]


def actualizar_pelicula(peliculas, id_pelicula, titulo=None, genero=None, duracion=None, precio=None):
    """Actualiza los campos de una película existente."""
    pelicula = obtener_pelicula(peliculas, id_pelicula)
    
    if pelicula is None:
        return False

    pelicula_original = pelicula.copy()

    if titulo is not None:
        titulo = titulo.strip()
        if len(titulo) > 50:
            titulo = titulo[:47] + "..."
    
    # Actualizar solo los campos no None
    if titulo is not None:
        pelicula["titulo"] = titulo
    if genero is not None:
        pelicula["genero"] = genero
    if duracion is not None:
        pelicula["duracion"] = duracion
    if precio is not None:
        pelicula["precio"] = precio

    if not guardar_peliculas(peliculas):
        pelicula.update(pelicula_original)
        return False
    
    return True


def eliminar_pelicula(peliculas, id_pelicula):
    """Elimina una película del catálogo por su ID."""

    for i in range(len(peliculas)):
        if peliculas[i]["id"] == id_pelicula:
            pelicula_eliminada = peliculas.pop(i)
            if not guardar_peliculas(peliculas):
                peliculas.insert(i, pelicula_eliminada)
                return False
            return True

    return False


def contar_peliculas(peliculas):
    """Retorna el total de películas en el catálogo."""
    return len(peliculas)


def promedio_duracion(peliculas):
    """Calcula el promedio de duración de todas las películas."""
    if len(peliculas) == 0:
        return 0
    
    total = 0
    for pelicula in peliculas:
        total += pelicula["duracion"]

    return total / len(peliculas)
