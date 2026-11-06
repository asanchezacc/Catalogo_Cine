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


def test_json_peliculas_danado_o_duplicado_no_se_reemplaza():
    from src.datos import datos_iniciales
    ruta_original = peliculas.ARCHIVO_PELICULAS
    peliculas.ARCHIVO_PELICULAS = "peliculas_pruebas_pytest.json"
    try:
        with open(peliculas.ARCHIVO_PELICULAS, "w", encoding="utf-8") as archivo:
            archivo.write("contenido incorrecto")
        catalogo = []
        assert datos_iniciales.cargar_peliculas(catalogo) is None
        with open(peliculas.ARCHIVO_PELICULAS, "r", encoding="utf-8") as archivo:
            assert archivo.readline() == "contenido incorrecto"

        with open(peliculas.ARCHIVO_PELICULAS, "w", encoding="utf-8") as archivo:
            archivo.write('[{"id": 1, "titulo": "A", "genero": "Accion", "duracion": 90, "precio": 1000}, '
                          '{"id": 1, "titulo": "B", "genero": "Drama", "duracion": 90, "precio": 1000}]')
        assert peliculas.cargar_peliculas_desde_json(catalogo) is False
        assert catalogo == []
    finally:
        peliculas.ARCHIVO_PELICULAS = ruta_original


def test_peliculas_no_permite_titulos_duplicados_desde_funciones():
    ruta_original = peliculas.ARCHIVO_PELICULAS
    peliculas.ARCHIVO_PELICULAS = "peliculas_pruebas_pytest.json"
    try:
        catalogo = []
        assert peliculas.agregar_pelicula(catalogo, 1, "Supergirl", "Accion", 90, 1000)
        assert not peliculas.agregar_pelicula(catalogo, 2, "supergirl", "Accion", 90, 1000)
        assert peliculas.agregar_pelicula(catalogo, 2, "Otra película", "Accion", 90, 1000)
        assert not peliculas.actualizar_pelicula(catalogo, 2, titulo="SUPERGIRL")
        assert catalogo[1]["titulo"] == "Otra película"
    finally:
        peliculas.ARCHIVO_PELICULAS = ruta_original


def test_modificar_pelicula_rechaza_genero_duracion_y_precio_invalidos():
    catalogo = [{
        "id": 1, "titulo": "La Odisea", "genero": "Drama",
        "duracion": 90, "precio": 2000,
    }]
    original = catalogo[0].copy()
    assert peliculas.actualizar_pelicula(catalogo, 1, genero="   ") is False
    assert peliculas.actualizar_pelicula(catalogo, 1, duracion=-10) is False
    assert peliculas.actualizar_pelicula(catalogo, 1, duracion="noventa") is False
    assert peliculas.actualizar_pelicula(catalogo, 1, precio=0) is False
    assert peliculas.actualizar_pelicula(catalogo, 1, precio="gratis") is False
    assert catalogo[0] == original
