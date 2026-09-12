from login import USUARIOS, buscar_usuario, agregar_usuario, eliminar_usuario, actualizar_usuario, iniciar_sesion, ver_historial
from validaciones import validar_contrasena
from reservas import (
    RESERVAS,
    crear_reserva,
    cobrar_reserva,
    imprimir_ticket,
    ver_reservas,
    ordenar_reservas_por_precio,
    clientes_con_reservas,
)
from estadisticas import resumen_estadisticas

PELICULAS = ["Película 1", "Película 2", "Película 3"]


def pedir_entero(mensaje):
    entrada = input(mensaje).strip()

    if not entrada.isdigit():
        return None

    return int(entrada)


def pedir_precio(mensaje):
    entrada = input(mensaje).strip()

    if not entrada.replace(".", "", 1).isdigit():
        return None

    return float(entrada)


def accion_ver_usuarios():
    lineas = map(lambda par: f"{par[0]} - {par[1]['rol']}", USUARIOS.items())
    for linea in lineas:
        print(linea)


def accion_agregar_usuario(usuario_actual):
    nuevo_usuario = input("Nombre de usuario nuevo: ").strip()

    if not nuevo_usuario:
        print("El nombre de usuario no puede estar vacío.")
        return

    contrasena = input("Contraseña: ")

    es_valida, mensaje = validar_contrasena(contrasena)
    if not es_valida:
        print(mensaje)
        return

    rol = input("Rol (empleado/cliente): ").strip().lower()

    exito, mensaje = agregar_usuario(usuario_actual, nuevo_usuario, contrasena, rol, USUARIOS)
    print(mensaje)


def accion_eliminar_usuario(usuario_actual):
    usuario_a_borrar = input("Usuario a borrar: ").strip()
    exito, mensaje = eliminar_usuario(usuario_actual, usuario_a_borrar, USUARIOS)
    print(mensaje)


def accion_cambiar_contrasena(usuario_actual):
    nueva_contrasena = input("Nueva contraseña: ")

    es_valida, mensaje = validar_contrasena(nueva_contrasena)
    if not es_valida:
        print(mensaje)
        return

    exito, mensaje = actualizar_usuario(usuario_actual, usuario_actual, nueva_contrasena, USUARIOS)
    print(mensaje)


def accion_ver_historial():
    entradas = ver_historial()

    if not entradas:
        print("No hay historial todavía.")
        return

    for accion, usuario, rol in entradas:
        print(f"{accion} - {usuario} ({rol})")


def accion_clientes_sin_reservar():
    todos_los_clientes = set([usuario for usuario, datos in USUARIOS.items() if datos["rol"] == "cliente"])
    con_reserva = clientes_con_reservas(RESERVAS)
    sin_reservar = todos_los_clientes - con_reserva

    if not sin_reservar:
        print("Todos los clientes ya reservaron alguna vez.")
        return

    for cliente in sin_reservar:
        print(cliente)


def accion_ver_estadisticas():
    resumen = resumen_estadisticas(RESERVAS)

    print(f"Precio promedio: ${resumen['promedio_precio']:.2f}")
    print(f"Reservas pendientes: {resumen['cantidad_pendientes']}")
    print(f"Reservas cobradas: {resumen['cantidad_cobradas']}")
    print(f"Porcentaje cobradas: {resumen['porcentaje_cobradas']:.1f}%")
    print(f"Total recaudado: ${resumen['total_recaudado']}")


def accion_ver_reservas(empleado=None, cliente=None):
    encontradas = ver_reservas(RESERVAS, empleado=empleado, cliente=cliente)

    if not encontradas:
        print("No hay reservas para mostrar.")
        return

    lineas = map(
        lambda fila: f"#{fila[0]} - {fila[2]} - cliente: {fila[1]} - estado: {fila[5]}",
        encontradas,
    )
    for linea in lineas:
        print(linea)


def accion_ver_reservas_ordenadas():
    ordenadas = ordenar_reservas_por_precio(RESERVAS, descendente=True)

    if not ordenadas:
        print("No hay reservas para mostrar.")
        return

    lineas = map(
        lambda fila: f"#{fila[0]} - {fila[2]} - ${fila[4]} - estado: {fila[5]}",
        ordenadas,
    )
    for linea in lineas:
        print(linea)


def accion_dar_reserva(usuario_actual):
    nombre_cliente = input("Usuario del cliente: ").strip()
    datos_cliente = buscar_usuario(nombre_cliente, USUARIOS)

    if datos_cliente is None or datos_cliente["rol"] != "cliente":
        print("Ese usuario no existe o no es un cliente.")
        return

    print("Películas disponibles:", ", ".join(PELICULAS))
    pelicula = input("Película a reservar: ").strip()

    if pelicula not in PELICULAS:
        print("Esa película no está en el catálogo.")
        return

    precio = pedir_precio("Precio: ")

    if precio is None:
        print("Ingresá un precio válido.")
        return

    id_reserva, mensaje = crear_reserva(nombre_cliente, pelicula, usuario_actual, precio, RESERVAS)
    print(mensaje)


def accion_reservar_como_cliente(usuario_actual):
    print("Películas disponibles:", ", ".join(PELICULAS))
    pelicula = input("Película a reservar: ").strip()

    if pelicula not in PELICULAS:
        print("Esa película no está en el catálogo.")
        return

    id_reserva, mensaje = crear_reserva(usuario_actual, pelicula, None, 0, RESERVAS)
    print(mensaje)
    print("Queda pendiente de cobro por un empleado.")


def accion_cobrar_reserva(usuario_actual):
    id_reserva = pedir_entero("Número de reserva a cobrar: ")

    if id_reserva is None:
        print("Ingresá un número de reserva válido.")
        return

    exito, mensaje = cobrar_reserva(id_reserva, RESERVAS, empleado=usuario_actual)
    print(mensaje)


def accion_imprimir_ticket():
    id_reserva = pedir_entero("Número de reserva: ")

    if id_reserva is None:
        print("Ingresá un número de reserva válido.")
        return

    exito, resultado = imprimir_ticket(id_reserva, RESERVAS)
    print(resultado)


def menu_administrador(usuario_actual):
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Ver usuarios")
        print("2. Dar de alta un usuario")
        print("3. Borrar un usuario")
        print("4. Ver reservas")
        print("5. Ver reservas ordenadas por precio")
        print("6. Ver historial de usuarios")
        print("7. Ver clientes que nunca reservaron")
        print("8. Ver estadísticas")
        print("9. Cambiar mi contraseña")
        print("10. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            accion_ver_usuarios()
        elif opcion == "2":
            accion_agregar_usuario(usuario_actual)
        elif opcion == "3":
            accion_eliminar_usuario(usuario_actual)
        elif opcion == "4":
            accion_ver_reservas()
        elif opcion == "5":
            accion_ver_reservas_ordenadas()
        elif opcion == "6":
            accion_ver_historial()
        elif opcion == "7":
            accion_clientes_sin_reservar()
        elif opcion == "8":
            accion_ver_estadisticas()
        elif opcion == "9":
            accion_cambiar_contrasena(usuario_actual)
        elif opcion == "10":
            print("Cerrando sesión.")
            break
        else:
            print("Opción inválida.")


def menu_empleado(usuario_actual):
    while True:
        print("\n--- MENÚ EMPLEADO ---")
        print("1. Dar una reserva")
        print("2. Cobrar una reserva")
        print("3. Imprimir ticket")
        print("4. Ver reservas")
        print("5. Ver reservas ordenadas por precio")
        print("6. Borrar un cliente")
        print("7. Darme de baja")
        print("8. Cambiar mi contraseña")
        print("9. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            accion_dar_reserva(usuario_actual)
        elif opcion == "2":
            accion_cobrar_reserva(usuario_actual)
        elif opcion == "3":
            accion_imprimir_ticket()
        elif opcion == "4":
            accion_ver_reservas()
        elif opcion == "5":
            accion_ver_reservas_ordenadas()
        elif opcion == "6":
            accion_eliminar_usuario(usuario_actual)
        elif opcion == "7":
            exito, mensaje = eliminar_usuario(usuario_actual, usuario_actual, USUARIOS)
            print(mensaje)
            if exito:
                break
        elif opcion == "8":
            accion_cambiar_contrasena(usuario_actual)
        elif opcion == "9":
            print("Cerrando sesión.")
            break
        else:
            print("Opción inválida.")


def menu_cliente(usuario_actual):
    while True:
        print("\n--- MENÚ CLIENTE ---")
        print("1. Ver catálogo de películas")
        print("2. Reservar una película")
        print("3. Ver mis reservas")
        print("4. Cambiar mi contraseña")
        print("5. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            print("Películas disponibles:", ", ".join(PELICULAS))
        elif opcion == "2":
            accion_reservar_como_cliente(usuario_actual)
        elif opcion == "3":
            accion_ver_reservas(cliente=usuario_actual)
        elif opcion == "4":
            accion_cambiar_contrasena(usuario_actual)
        elif opcion == "5":
            print("Cerrando sesión.")
            break
        else:
            print("Opción inválida.")


def main():
    usuario, rol = iniciar_sesion()

    if usuario is None:
        return

    if rol == "administrador":
        menu_administrador(usuario)
    elif rol == "empleado":
        menu_empleado(usuario)
    elif rol == "cliente":
        menu_cliente(usuario)


if __name__ == "__main__":
    main()
