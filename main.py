"""
SISTEMA DE GESTIÓN DE CINE
Punto de entrada del programa - Test CRUD Películas
"""

from src.vista import imprimir_encabezado, imprimir_exito, imprimir_error
from src.funciones.peliculas import agregar_pelicula, listar_peliculas, contar_peliculas, promedio_duracion
from src.datos.datos_iniciales import peliculas_iniciales

if __name__ == "__main__":
    imprimir_encabezado("Sistema de Cine - Test CRUD Películas")
    
    # Copiar datos iniciales
    peliculas = [p.copy() for p in peliculas_iniciales]
    
    # Mostrar estadísticas
    print(f"Total de películas: {contar_peliculas(peliculas)}")
    print(f"Promedio de duración: {promedio_duracion(peliculas):.1f} minutos\n")
    
    # Listar películas
    print("--- CATÁLOGO INICIAL ---")
    for p in listar_peliculas(peliculas):
        print(f"ID: {p['id']} | {p['titulo']} ({p['duracion']} min) | ${p['precio']}")
    
    # Agregar nueva película
    print("\n--- AGREGANDO NUEVA PELÍCULA ---")
    resultado = agregar_pelicula(peliculas, 6, "Avatar", "Ciencia ficción", 162, 260)
    if resultado:
        imprimir_exito(f"Película agregada. Total: {contar_peliculas(peliculas)}")
    else:
        imprimir_error("No se pudo agregar")
    
    # Listar de nuevo
    print("\n--- CATÁLOGO ACTUALIZADO ---")
    for p in listar_peliculas(peliculas):
        print(f"ID: {p['id']} | {p['titulo']} ({p['duracion']} min) | ${p['precio']}")
