import pytest
import json
from src.modelos import clientes

def setup_function():
    """Se ejecuta antes de cada prueba para limpiar los datos."""
    clientes.lista_clientes.clear()
    clientes.emails_activos.clear()

    # Usamos un JSON temporal para no pisar el archivo real del proyecto
    clientes.ARCHIVO_CLIENTES = "test_clientes_temporal.json"

    # Vaciamos el archivo temporal
    try:
        with open(clientes.ARCHIVO_CLIENTES, "w", encoding="UTF-8") as archivo:
            archivo.write("[]")
    except OSError:
        pass # Si falla, el alta_cliente se va a encargar de crearlo luego

def test_alta_cliente_exitosa():
    resultado = clientes.alta_cliente("Test User", "test@mail.com", "12345678", False)
    assert resultado is True
    assert len(clientes.lista_clientes) == 1
    assert clientes.lista_clientes[0]["nombre"] == "Test User"

def test_alta_cliente_email_duplicado():
    clientes.alta_cliente("User 1", "duplicado@mail.com", "1122334455", False)
    resultado = clientes.alta_cliente("User 2", "duplicado@mail.com", "1122334466", False)
    assert resultado is False
    assert len(clientes.lista_clientes) == 1 

def test_recursividad_suma_digitos():
    assert clientes.sumar_digitos_telefono_recursivo("12345") == 15
    assert clientes.sumar_digitos_telefono_recursivo("") == 0

def test_slicing_listar_paginado():
    clientes.alta_cliente("Cliente A", "a@mail.com", "1122334455", False)
    clientes.alta_cliente("Cliente B", "b@mail.com", "1122334466", False)
    clientes.alta_cliente("Cliente C", "c@mail.com", "1122334477", False)

    pagina_1 = clientes.listar_clientes_paginado(0, 2)
    assert len(pagina_1) == 2
    assert pagina_1[0]["nombre"] == "Cliente A"
    assert pagina_1[1]["nombre"] == "Cliente B"


def test_json_danado_no_reemplaza_clientes():
    assert clientes.alta_cliente("Cliente", "cliente@mail.com", "12345678", False)
    with open(clientes.ARCHIVO_CLIENTES, "w", encoding="utf-8") as archivo:
        archivo.write("datos dañados")
    assert clientes.cargar_clientes_desde_json() is False
    assert len(clientes.lista_clientes) == 1
    assert clientes.lista_clientes[0]["email"] == "cliente@mail.com"


def test_error_guardado_alta_no_confirma_cliente():
    clientes.ARCHIVO_CLIENTES = "src/datos"
    assert clientes.alta_cliente("Cliente", "cliente@mail.com", "12345678", False) is False
    assert clientes.lista_clientes == []
    assert clientes.emails_activos == set()


def test_error_guardado_baja_restaura_estado():
    assert clientes.alta_cliente("Cliente", "cliente@mail.com", "12345678", False)
    clientes.ARCHIVO_CLIENTES = "src/datos"
    assert clientes.baja_cliente(1) is False
    assert clientes.buscar_cliente(1)["estado"] is True


def test_modificacion_invalida_no_cambia_email():
    assert clientes.alta_cliente("Cliente", "cliente@mail.com", "12345678", False)
    assert clientes.modificar_cliente(1, nombre=" ", email="otro@mail.com") is False
    assert clientes.buscar_cliente(1)["email"] == "cliente@mail.com"
    assert clientes.emails_activos == {"cliente@mail.com"}


def test_error_guardado_modificacion_restaura_datos():
    assert clientes.alta_cliente("Cliente", "cliente@mail.com", "12345678", False)
    clientes.ARCHIVO_CLIENTES = "src/datos"
    assert clientes.modificar_cliente(1, nombre="Otro", email="otro@mail.com") is False
    assert clientes.buscar_cliente(1)["nombre"] == "Cliente"
    assert clientes.buscar_cliente(1)["email"] == "cliente@mail.com"
    assert clientes.emails_activos == {"cliente@mail.com"}


def test_contar_clientes_recursivo():
    assert clientes.contar_clientes_recursivo([]) == 0
    lista = [{"id": 1}, {"id": 2}, {"id": 3}]
    assert clientes.contar_clientes_recursivo(lista) == 3


def test_alta_rechaza_telefono_invalido():
    assert clientes.alta_cliente("Cliente", "cliente@mail.com", "abc", False) is False
    assert clientes.lista_clientes == []
    assert clientes.emails_activos == set()


def test_modificacion_rechaza_telefono_invalido_sin_cambiar_datos():
    assert clientes.alta_cliente("Cliente", "cliente@mail.com", "1122334455", False)
    assert clientes.modificar_cliente(1, email="otro@mail.com", telefono="123") is False
    assert clientes.buscar_cliente(1)["telefono"] == "1122334455"
    assert clientes.buscar_cliente(1)["email"] == "cliente@mail.com"
    assert clientes.emails_activos == {"cliente@mail.com"}


def test_alta_id_no_repite_si_hay_huecos():
    assert clientes.alta_cliente("Cliente A", "a@mail.com", "1122334455", False)
    assert clientes.alta_cliente("Cliente B", "b@mail.com", "1122334466", False)
    clientes.lista_clientes[1]["id"] = 5
    assert clientes.alta_cliente("Cliente C", "c@mail.com", "1122334477", False)
    assert [cliente["id"] for cliente in clientes.lista_clientes] == [1, 5, 6]


def test_alta_email_duplicado_cambiando_mayusculas():
    assert clientes.alta_cliente("Cliente A", "Cliente@Mail.com", "1122334455", False)
    assert clientes.alta_cliente("Cliente B", "cliente@mail.com", "1122334466", False) is False
    assert len(clientes.lista_clientes) == 1


def test_modificacion_email_duplicado_cambiando_mayusculas():
    assert clientes.alta_cliente("Cliente A", "a@mail.com", "1122334455", False)
    assert clientes.alta_cliente("Cliente B", "b@mail.com", "1122334466", False)
    assert clientes.modificar_cliente(2, email="A@MAIL.COM") is False
    assert clientes.buscar_cliente(2)["email"] == "b@mail.com"


def test_carga_json_rechaza_emails_duplicados_por_mayusculas():
    assert clientes.alta_cliente("Cliente A", "a@mail.com", "1122334455", False)
    assert clientes.alta_cliente("Cliente B", "b@mail.com", "1122334466", False)
    datos = [
        {"id": 1, "nombre": "A", "email": "a@mail.com", "telefono": "1122334455", "estado": True},
        {"id": 2, "nombre": "B", "email": "A@MAIL.COM", "telefono": "1122334466", "estado": True},
    ]
    with open(clientes.ARCHIVO_CLIENTES, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo)
    assert clientes.cargar_clientes_desde_json() is False
    assert len(clientes.lista_clientes) == 2


def test_telefono_solo_permite_mas_al_principio():
    assert clientes.alta_cliente("Cliente", "cliente@mail.com", "123+456789", False) is False
    assert clientes.alta_cliente("Cliente", "cliente@mail.com", "+54 11 1234-5678", False) is True


def test_reserva_rechaza_cliente_inactivo_desde_funcion():
    from src.funciones import empleados, asientos
    # Se comprueba la regla aun cuando no se utiliza la opción del menú.
    clientes.lista_clientes.append({
        "id": 8, "nombre": "Cliente inactivo", "email": "inactivo@mail.com",
        "telefono": "1122334455", "estado": False
    })
    sala = asientos.crear_sala(2, 2)
    exito, mensaje = empleados.dar_reserva(sala, 8, 1, 2500, 0, 0, 1)
    assert exito is False
    assert "baja" in mensaje
    assert asientos.contar_asientos_libres(sala) == 4
