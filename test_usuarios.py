import pytest

from src.modelos import usuarios
from src.validaciones import contar_mayusculas_recursivo, validar_contrasena


@pytest.fixture(autouse=True)
def usuarios_limpios(tmp_path, monkeypatch):
    """Antes de cada prueba: lista vacía y un JSON temporal (no toca el usuarios.json real)."""
    monkeypatch.setattr(usuarios, "ARCHIVO_USUARIOS", str(tmp_path / "usuarios.json"))
    usuarios.usuarios.clear()
    usuarios.HISTORIAL.clear()
    yield
    usuarios.usuarios.clear()
    usuarios.HISTORIAL.clear()


def test_alta_usuario_correcta():
    exito, resultado = usuarios.alta_usuario("Ana Gomez", "ana", "Clave123!", "empleado")

    assert exito == True
    assert resultado["id"] == 1
    assert usuarios.buscar_usuario("ana") is not None


def test_alta_usuario_duplicado_es_rechazado():
    usuarios.alta_usuario("Ana Gomez", "ana", "Clave123!", "empleado")

    exito, mensaje = usuarios.alta_usuario("Otra Ana", "ana", "Clave456!", "empleado")

    assert exito == False
    assert mensaje == "Ese nombre de usuario ya existe."
    assert len(usuarios.usuarios) == 1


def test_credenciales_incorrectas_devuelven_false():
    usuarios.alta_usuario("Ana Gomez", "ana", "Clave123!", "empleado")

    exito_pass, _ = usuarios.verificar_credenciales("ana", "mala")
    exito_user, _ = usuarios.verificar_credenciales("nadie", "Clave123!")

    assert exito_pass == False
    assert exito_user == False


def test_credenciales_correctas_devuelven_el_rol():
    usuarios.alta_usuario("Ana Gomez", "ana", "Clave123!", "empleado")

    assert usuarios.verificar_credenciales("ana", "Clave123!") == (True, "empleado")


def test_baja_usuario_inexistente():
    exito, mensaje = usuarios.baja_usuario("fantasma")

    assert exito == False
    assert mensaje == "Usuario no encontrado."


def test_json_guarda_y_recupera_los_usuarios():
    usuarios.alta_usuario("Ana Gomez", "ana", "Clave123!", "empleado")
    usuarios.alta_usuario("Luis Paz", "luis", "Clave456!", "administrador")

    # Se vacía la memoria y se vuelve a cargar desde el archivo
    usuarios.usuarios.clear()
    exito, _ = usuarios.cargar_usuarios_desde_json()

    assert exito == True
    assert len(usuarios.usuarios) == 2
    assert usuarios.buscar_usuario("luis")["rol"] == "administrador"


def test_cargar_json_inexistente_no_rompe():
    exito, _ = usuarios.cargar_usuarios_desde_json()

    assert exito == True
    assert usuarios.usuarios == []


def test_cargar_json_danado_avisa_el_error(tmp_path):
    with open(usuarios.ARCHIVO_USUARIOS, "w", encoding="UTF-8") as archivo:
        archivo.write("esto no es un json {")

    exito, mensaje = usuarios.cargar_usuarios_desde_json()

    assert exito == False
    assert "No se pudieron cargar" in mensaje


def test_contar_mayusculas_recursivo():
    assert contar_mayusculas_recursivo("") == 0
    assert contar_mayusculas_recursivo("hola") == 0
    assert contar_mayusculas_recursivo("HoLa Mundo") == 3


def test_validar_contrasena_sin_mayuscula():
    exito, mensaje = validar_contrasena("clave123!")

    assert exito == False
    assert mensaje == "La contraseña debe tener al menos una mayúscula."