from src.funciones import peliculas


def test_agregar_pelicula_y_recortar_titulo():
    ruta_original = peliculas.ARCHIVO_PELICULAS
    catalogo_original = []
    peliculas.cargar_peliculas_desde_json(catalogo_original)
    catalogo = []
    titulo_largo = "El Señor de los Anillos: La Comunidad del Anillo - Edición Especial"

    try:
        peliculas.ARCHIVO_PELICULAS = ruta_original
        resultado = peliculas.agregar_pelicula(
            catalogo, 1, titulo_largo, "Fantasia", 178, 2500
        )

        assert resultado is True
        assert len(catalogo[0]["titulo"]) == 50
        assert catalogo[0]["titulo"].endswith("...")
    finally:
        peliculas.guardar_peliculas(catalogo_original)
        peliculas.ARCHIVO_PELICULAS = ruta_original


def test_cargar_modificar_y_eliminar_pelicula():
    ruta_original = peliculas.ARCHIVO_PELICULAS
    catalogo_original = []
    peliculas.cargar_peliculas_desde_json(catalogo_original)
    catalogo = [{
        "id": 1,
        "titulo": "La Odisea",
        "genero": "Drama",
        "duracion": 90,
        "precio": 2000,
    }]

    try:
        peliculas.ARCHIVO_PELICULAS = ruta_original
        assert peliculas.guardar_peliculas(catalogo) is True

        cargadas = []
        assert peliculas.cargar_peliculas_desde_json(cargadas) is True
        assert cargadas[0]["titulo"] == "La Odisea"

        assert peliculas.actualizar_pelicula(
            cargadas, 1, titulo="La Odisea Nueva"
        ) is True
        assert cargadas[0]["titulo"] == "La Odisea Nueva"

        assert peliculas.eliminar_pelicula(cargadas, 1) is True
        assert cargadas == []
    finally:
        peliculas.guardar_peliculas(catalogo_original)
        peliculas.ARCHIVO_PELICULAS = ruta_original
