
import unittest
import os
from src.funciones import tickets, asientos


class TestIntegracionTicketsAsientos(unittest.TestCase):

    def setUp(self):
        """Prepara los datos para cada prueba."""
        self.ruta_original = tickets.ARCHIVO_TICKETS
        self.tickets_originales = tickets.tickets_registrados[:]
        self.archivo_prueba = "tickets_integracion_prueba.txt"

        with open(self.archivo_prueba, "x", encoding="utf-8"):
            pass

        tickets.ARCHIVO_TICKETS = self.archivo_prueba
        tickets.tickets_registrados.clear()

    def tearDown(self):
        """Restaura los datos y elimina el archivo de prueba."""
        tickets.ARCHIVO_TICKETS = self.ruta_original
        tickets.tickets_registrados[:] = self.tickets_originales
        os.remove(self.archivo_prueba)

    def test_reinicio_recupera_asientos(self):
        """Recupera los asientos usando los tickets guardados."""

        # Creamos tres tickets
        exito, id_1 = tickets.crear_ticket(1, 2, (0, 0), 2500, 1)
        self.assertTrue(exito)

        exito, id_2 = tickets.crear_ticket(2, 2, (0, 1), 2500, 1)
        self.assertTrue(exito)

        exito, id_3 = tickets.crear_ticket(3, 2, (1, 2), 2500, 1)
        self.assertTrue(exito)

        # Cobramos uno y cancelamos otro
        self.assertTrue(tickets.cobrar(id_2)[0])
        self.assertTrue(tickets.cancelar_ticket(id_3)[0])

        # Simulamos reiniciar el programa
        tickets.tickets_registrados.clear()
        sala = asientos.crear_sala(2, 3)

        # Recuperamos los tickets y los asientos
        self.assertTrue(tickets.cargar_tickets()[0])

        resultado, mensaje = asientos.reconstruir_ocupacion(
            sala, tickets.tickets_registrados
        )

        self.assertTrue(resultado)

        # Verificamos los dos asientos ocupados
        self.assertEqual(
            asientos.obtener_estado_asiento(sala, 0, 0),
            asientos.ASIENTO_OCUPADO
        )

        self.assertEqual(
            asientos.obtener_estado_asiento(sala, 0, 1),
            asientos.ASIENTO_OCUPADO
        )

        # El asiento cancelado debe estar libre
        self.assertEqual(
            asientos.obtener_estado_asiento(sala, 1, 2),
            asientos.ASIENTO_LIBRE
        )

        self.assertEqual(asientos.contar_asientos_libres(sala), 4)

    def test_reinicio_detecta_duplicados(self):
        """Detecta dos tickets activos para el mismo asiento."""

        self.assertTrue(
            tickets.crear_ticket(1, 2, (0, 0), 2500, 1)[0]
        )
        self.assertTrue(
            tickets.crear_ticket(2, 2, (0, 0), 2500, 1)[0]
        )

        tickets.tickets_registrados.clear()

        sala = asientos.crear_sala(2, 3)
        sala_anterior = [fila[:] for fila in sala]

        self.assertTrue(tickets.cargar_tickets()[0])

        resultado, mensaje = asientos.reconstruir_ocupacion(
            sala, tickets.tickets_registrados
        )

        self.assertFalse(resultado)
        self.assertEqual(sala, sala_anterior)


if __name__ == "__main__":
    unittest.main()

