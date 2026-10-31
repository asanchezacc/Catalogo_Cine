
import unittest
from src.funciones import asientos


class TestAsientos(unittest.TestCase):

    def setUp(self):

        """Crea una sala nueva antes de cada prueba."""

        self.sala = asientos.crear_sala(2, 3)



    def test_sala_inicial(self):

        """Comprueba que todos los asientos comiencen libres."""

        libres = asientos.contar_asientos_libres(self.sala)
        self.assertEqual(libres, 6)



    def test_ocupar_asiento(self):

        """Comprueba que ocupar un asiento reduzca los libres."""

        asientos.ocupar_asiento(self.sala, 0, 1)

        libres = asientos.contar_asientos_libres(self.sala)
        self.assertEqual(libres, 5)



    def test_liberar_asiento(self):

        """Comprueba que liberar un asiento aumente los libres."""

        asientos.ocupar_asiento(self.sala, 0, 1)
        asientos.liberar_asiento(self.sala, 0, 1)

        libres = asientos.contar_asientos_libres(self.sala)
        self.assertEqual(libres, 6)



    def test_sala_vacia(self):

        """Comprueba que una sala sin filas devuelva cero."""

        libres = asientos.contar_asientos_libres([])
        self.assertEqual(libres, 0)



    def test_recuperar_asientos(self):

        """Comprueba la ocupacion a partir de tickets."""

        lista_tickets = [
            {"id": 1, "asiento": (0, 1), "estado": "pendiente"},
            {"id": 2, "asiento": (1, 2), "estado": "cobrado"},
            {"id": 3, "asiento": (0, 2), "estado": "cancelado"}
        ]

        resultado, mensaje = asientos.reconstruir_ocupacion(
            self.sala, lista_tickets
        )

        self.assertTrue(resultado)

        # Dos asientos ocupados, cuatro libres
        self.assertEqual(
            asientos.contar_asientos_libres(self.sala), 4
        )

        # El ticket cancelado no ocupa asiento
        self.assertEqual(
            asientos.obtener_estado_asiento(self.sala, 0, 2),
            asientos.ASIENTO_LIBRE
        )



    def test_asientos_duplicados(self):

        """Comprueba que no se acepten dos reservas del mismo asiento."""

        lista_tickets = [
            {"id": 1, "asiento": (0, 1), "estado": "pendiente"},
            {"id": 2, "asiento": (0, 1), "estado": "cobrado"}
        ]

        sala_original = [fila[:] for fila in self.sala]

        resultado, mensaje = asientos.reconstruir_ocupacion(
            self.sala, lista_tickets
        )

        self.assertFalse(resultado)
        self.assertEqual(self.sala, sala_original)


    def test_asiento_fuera_de_rango(self):
        
        """Comprueba que se detecten coordenadas invalidas."""

        lista_tickets = [
            {"id": 1, "asiento": (5, 0), "estado": "pendiente"}
        ]

        sala_original = [fila[:] for fila in self.sala]

        resultado, mensaje = asientos.reconstruir_ocupacion(
            self.sala, lista_tickets
        )

        self.assertFalse(resultado)
        self.assertEqual(self.sala, sala_original)



if __name__ == "__main__":
    unittest.main()

