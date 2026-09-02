"""
CRUD de películas
Funciones para agregar, leer, actualizar y eliminar películas
"""

def agregar_pelicula(peliculas, id_pelicula, titulo, genero, duracion, precio):
    """Agrega una nueva película al catálogo si el ID no existe."""
    # Verificar si el ID ya existe
    for pelicula in peliculas:
        if pelicula["id"] == id_pelicula:
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
    return True


def obtener_pelicula(peliculas, id_pelicula):
    """Obtiene una película por su ID, devuelve None si no existe."""
    for pelicula in peliculas:
        if pelicula["id"] == id_pelicula:
            return pelicula
    return None


def listar_peliculas(peliculas):
    """Devuelve una copia de la lista completa de películas."""
    return peliculas[:]  # Devolver una copia


def actualizar_pelicula(peliculas, id_pelicula, titulo=None, genero=None, duracion=None, precio=None):
    """Actualiza los campos de una película existente."""
    pelicula = obtener_pelicula(peliculas, id_pelicula)
    
    if pelicula is None:
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
    
    return True


def eliminar_pelicula(peliculas, id_pelicula):
    """Elimina una película del catálogo por su ID."""
    for i, pelicula in enumerate(peliculas):
        if pelicula["id"] == id_pelicula:
            peliculas.pop(i)
            return True
    return False


def contar_peliculas(peliculas):
    """Retorna el total de películas en el catálogo."""
    return len(peliculas)


def promedio_duracion(peliculas):
    """Calcula el promedio de duración de todas las películas."""
    if len(peliculas) == 0:
        return 0
    
    total = sum(p["duracion"] for p in peliculas)
    return total / len(peliculas)
