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
    """Carga las películas; True si carga, None si falta el archivo y False si es inválido."""
    try:
        with open(ARCHIVO_PELICULAS, "r", encoding="UTF-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return None
    except (OSError, ValueError, TypeError, UnicodeError):
        return False

    if type(datos) != list:
        return False

    ids = set()
    titulos = set()
    for pelicula in datos:
        if type(pelicula) != dict:
            return False
        for campo in ("id", "titulo", "genero", "duracion", "precio"):
            if campo not in pelicula:
                return False

        id_pelicula = pelicula["id"]
        titulo = pelicula["titulo"]
        genero = pelicula["genero"]
        duracion = pelicula["duracion"]
        precio = pelicula["precio"]

        if type(id_pelicula) != int or id_pelicula <= 0 or id_pelicula in ids:
            return False
        if type(titulo) != str or not titulo.strip() or len(titulo) > 50:
            return False
        if titulo.lower() in titulos:
            return False
        if type(genero) != str or not genero.strip():
            return False
        if type(duracion) != int or duracion <= 0:
            return False
        if type(precio) not in (int, float) or precio <= 0:
            return False

        ids.add(id_pelicula)
        titulos.add(titulo.lower())

    peliculas[:] = datos
    return True


def agregar_pelicula(peliculas, id_pelicula, titulo, genero, duracion, precio):
    """Agrega una nueva película al catálogo si el ID no existe."""
    if type(id_pelicula) != int or id_pelicula <= 0:
        return False
    if type(titulo) != str or not titulo.strip():
        return False
    if type(genero) != str or not genero.strip():
        return False
    if type(duracion) != int or duracion <= 0:
        return False
    if type(precio) not in (int, float) or precio <= 0:
        return False

    titulo = titulo.strip()
    if len(titulo) > 50:
        titulo = titulo[:47] + "..."

    for pelicula in peliculas:
        if pelicula["id"] == id_pelicula or pelicula["titulo"].lower() == titulo.lower():
            return False
    
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

    # Validar primero todos los datos para no guardar valores incorrectos.
    if genero is not None:
        if type(genero) != str or not genero.strip():
            return False
        genero = genero.strip()
    if duracion is not None and (type(duracion) != int or duracion <= 0):
        return False
    if precio is not None and (type(precio) not in (int, float) or precio <= 0):
        return False

    pelicula_original = pelicula.copy()

    if titulo is not None:
        if type(titulo) != str or not titulo.strip():
            return False
        titulo = titulo.strip()
        if len(titulo) > 50:
            titulo = titulo[:47] + "..."
        for otra in peliculas:
            if otra["id"] != id_pelicula and otra["titulo"].lower() == titulo.lower():
                return False
    
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
