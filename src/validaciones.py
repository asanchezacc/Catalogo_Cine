import re


def validar_email(email):
    email = email.strip()
    patron = r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$"

    if re.match(patron, email):
        return True, "Email válido."

    return False, "El email no tiene un formato válido (ej: usuario@dominio.com)."


def validar_telefono(telefono, longitud_minima=8, longitud_maxima=15):
    solo_numeros = re.sub(r"[\s\-+]", "", telefono)

    if not re.match(r"^\d+$", solo_numeros):
        return False, "El teléfono solo puede tener números (espacios, guiones o un '+' inicial están permitidos)."

    if len(solo_numeros) < longitud_minima or len(solo_numeros) > longitud_maxima:
        return False, f"El teléfono debe tener entre {longitud_minima} y {longitud_maxima} dígitos."

    return True, "Teléfono válido."


def validar_contrasena(contrasena, longitud_minima=8):
    if len(contrasena) < longitud_minima:
        return False, f"La contraseña debe tener al menos {longitud_minima} caracteres."

    reglas = [
        (r"[A-Z]", "La contraseña debe tener al menos una mayúscula."),
        (r"[a-z]", "La contraseña debe tener al menos una minúscula."),
        (r"\d", "La contraseña debe tener al menos un número."),
        (r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", "La contraseña debe tener al menos un carácter especial."),
    ]

    for patron, mensaje in reglas:
        if not re.search(patron, contrasena):
            return False, mensaje

    return True, "Contraseña válida."
