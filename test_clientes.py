import pytest
import os
from src.modelos import clientes

def setup_function():
    """Se ejecuta antes de cada prueba."""
    clientes.lista_clientes.clear()
    clientes.emails_activos.clear()
    # Usamos un JSON temporal para que los tests NO pisen el archivo real del proyecto
    clientes.ARCHIVO_CLIENTES = "test_clientes_temporal.json"

def teardown_function():
    """Se ejecuta después de cada prueba para borrar el JSON temporal"""
    if os.path.exists("test_clientes_temporal.json"):
        os.remove("test_clientes_temporal.json")

def test_alta_cliente_exitosa():
    resultado = clientes.alta_cliente("Test User", "test@mail.com", "12345678", False)
    assert resultado is True
    assert len(clientes.lista_clientes) == 1
    assert clientes.lista_clientes[0]["nombre"] == "Test User"

def test_alta_cliente_email_duplicado():
    clientes.alta_cliente("User 1", "duplicado@mail.com", "1111", False)
    resultado = clientes.alta_cliente("User 2", "duplicado@mail.com", "2222", False)
    assert resultado is False
    assert len(clientes.lista_clientes) == 1 

def test_recursividad_suma_digitos():
    assert clientes.sumar_digitos_telefono_recursivo("12345") == 15
    assert clientes.sumar_digitos_telefono_recursivo("") == 0

def test_slicing_listar_paginado():
    clientes.alta_cliente("Cliente A", "a@mail.com", "111", False)
    clientes.alta_cliente("Cliente B", "b@mail.com", "222", False)
    clientes.alta_cliente("Cliente C", "c@mail.com", "333", False)
    
    pagina_1 = clientes.listar_clientes_paginado(0, 2)
    assert len(pagina_1) == 2
    assert pagina_1[0]["nombre"] == "Cliente A"
