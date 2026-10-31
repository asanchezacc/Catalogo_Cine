
import unittest
import os
from src.funciones import tickets


class TestTickets(unittest.TestCase):

    def setUp(self):


        """Prepara los datos antes de cada prueba."""


        self.ruta_original = tickets.ARCHIVO_TICKETS
        self.ruta_prueba = "tickets_unittest_local.txt"

        # No sobrescribimos archivos existentes.
        with open(self.ruta_prueba, "x", encoding="utf-8"):
            pass

        tickets.ARCHIVO_TICKETS = self.ruta_prueba
        tickets.tickets_registrados.clear()



    def tearDown(self):


        """Limpia los datos al terminar cada prueba."""


        tickets.tickets_registrados.clear()
        tickets.ARCHIVO_TICKETS = self.ruta_original
        os.remove(self.ruta_prueba)



    def test_crear_y_recuperar_ticket(self):


        """Comprueba que un ticket se guarda y recupera."""


        resultado, id_ticket = tickets.crear_ticket(
            1, 2, (0, 3), 2500, 1
        )

        self.assertTrue(resultado)
        self.assertEqual(id_ticket, 1)

        tickets.tickets_registrados.clear()
        resultado, mensaje = tickets.cargar_tickets()

        self.assertTrue(resultado)
        self.assertEqual(len(tickets.tickets_registrados), 1)
        self.assertEqual(
            tickets.tickets_registrados[0]["id"], 1
        )



    def test_cobrar_ticket(self):


        """Comprueba que el cobro queda guardado."""


        tickets.crear_ticket(1, 2, (0, 3), 2500, 1)

        resultado, mensaje = tickets.cobrar(1)
        self.assertTrue(resultado)

        tickets.tickets_registrados.clear()
        tickets.cargar_tickets()

        self.assertEqual(
            tickets.obtener_ticket(1)["estado"], "cobrado"
        )



    def test_cancelar_ticket(self):


        """Comprueba que la cancelacion queda guardada."""


        tickets.crear_ticket(1, 2, (0, 3), 2500, 1)

        resultado, mensaje = tickets.cancelar_ticket(1)
        self.assertTrue(resultado)

        tickets.tickets_registrados.clear()
        tickets.cargar_tickets()

        self.assertEqual(
            tickets.obtener_ticket(1)["estado"], "cancelado"
        )



    def test_archivo_danado(self):


        """Comprueba el manejo de un archivo incorrecto."""


        tickets.crear_ticket(1, 2, (0, 3), 2500, 1)

        with open(self.ruta_prueba, "w", encoding="utf-8") as archivo:
            archivo.write("datos|incorrectos\n")

        resultado, mensaje = tickets.cargar_tickets()

        self.assertFalse(resultado)
        self.assertEqual(len(tickets.tickets_registrados), 1)



    def test_error_guardado_al_crear(self):
        """Comprueba que un error al guardar no cree un ticket."""

        # Usamos una carpeta como ruta para provocar un error
        tickets.ARCHIVO_TICKETS = "src/datos"

        resultado, mensaje = tickets.crear_ticket(
            1, 2, (0, 3), 2500, 1
        )

        self.assertFalse(resultado)
        self.assertEqual(len(tickets.tickets_registrados), 0)


    def test_error_guardado_al_cobrar(self):
        """Comprueba que un cobro fallido conserve el estado."""

        tickets.crear_ticket(1, 2, (0, 3), 2500, 1)

        # Simulamos un error de escritura
        tickets.ARCHIVO_TICKETS = "src/datos"

        resultado, mensaje = tickets.cobrar(1)

        self.assertFalse(resultado)
        self.assertEqual(
            tickets.obtener_ticket(1)["estado"], "pendiente"
        )


    def test_error_guardado_al_cancelar(self):
        """Comprueba que una cancelacion fallida no cambie el estado."""

        tickets.crear_ticket(1, 2, (0, 3), 2500, 1)

        # Simulamos un error de escritura
        tickets.ARCHIVO_TICKETS = "src/datos"

        resultado, mensaje = tickets.cancelar_ticket(1)

        self.assertFalse(resultado)
        self.assertEqual(
            tickets.obtener_ticket(1)["estado"], "pendiente"
        )



if __name__ == "__main__":
    unittest.main()

