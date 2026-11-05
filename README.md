# **Sistema de Gestión de Cine (Catálogo de Cine)**

Sistema desarrollado en Python que permite administrar un cine (películas, clientes, sala de asientos y venta de tickets) mediante una interfaz de consola con roles de usuario.

Proyecto de la materia **Programación 1 - Algoritmos y Estructuras de Datos 1** (UADE).

---

## **Integrantes del Equipo (Equipo 6)**

- Cobos Caballero Katherine Beatriz
- Ridella Juan Manuel
- Sanchez Accinelli Antonio
- Zausa Martin Gustavo
- Magrone Juan Francisco

---

## **Funcionalidades Principales**

- Sistema de **Login con roles** (Administrador y Empleado).
- **CRUD completo** de Clientes y Películas, con baja lógica y validaciones.
- **Gestión de Sala** mediante matrices (lista de listas) para ocupar y liberar asientos.
- **Gestión de Tickets**: reserva, cobro, cancelación y búsquedas cruzadas A->B.
- **Módulo de estadísticas**: promedios, máximos/mínimos y recaudación.

---

## **Tecnologías y Conceptos Aplicados**

- **Python 3**
- **Persistencia de datos** mediante JSON (`json.load` y `json.dump`) y TXT para usuarios
- **Manejo de excepciones** (`try/except`, `raise`)
- **Recursividad** aplicada en tres casos: listas, matrices y cadenas
- **Expresiones regulares** para validaciones
- **Funciones lambda, `map`, `filter` y `reduce`**
- **Pruebas unitarias** con `pytest`

---

## **Cómo Ejecutar el Proyecto**

**Requisitos:**

- Python 3.x
- `pytest`

**Instalación de dependencias:**

```bash
pip install pytest
```

**Iniciar el sistema:**

```bash
python main.py
```

**Ejecutar los tests:**

```bash
pytest -v
```

---

## Credenciales iniciales

En la primera ejecución se crea `src/datos/usuarios.txt` si todavía no existe.

- **Administrador:** usuario `admin` / contraseña `admin123`
- **Empleado:** usuario `empleado1` / contraseña `1234`

Los usuarios que se den de alta y los cambios de contraseña se guardan en el archivo TXT. El archivo local de usuarios no se sube a GitHub.
