"""ARCHIVO CON UTILIDADES PARA MOSTRAR PROBLEMAS, COMPROBAR ROLES, USUARIOS, ..."""


"""muestra un problema dados los datos (arr, en bd.py). el nombre, y si queremos mostrar info o tex"""
def show_problem(arr, show_tex=True, show_info=True):
    if show_info:
        t = "**Nombre**: " + arr[0] + "\n"
        t += "**Propuesto por**: " + arr[1]
        t += "\n**Fuente**: " + arr[2]
        t += "\n**Link**: " + arr[3]
        if len(arr) == 6 and show_tex:
            t += "\n**Contenido (TEX)**:\n```tex\n" + arr[5] + "```" if arr[5] else ""
        return t
    else:
        return arr[3]  # solo el link a la imagen


"""esta función comprueba que tengamos permisos para hacer tales cambios"""
def check_rol(ctx, rol=["admin", "moderador"]):
    rol = [x.lower() for x in rol]  # pasamos todo a "lower"
    roles = [x.name.lower() for x in ctx.author.roles]  # obtenemos la lista de roles
    permisos = [x for x in rol if x in roles]  # cantidad de permisos que coinciden
    return len(permisos) > 0


"""inserta un blockquote"""
def block(texto, inline=True):
    if inline:
        return "\n```\n" + str(texto) + "\n```"
    else:
        return "```\n" + str(texto) + "\n```"
