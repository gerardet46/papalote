import sqlite3
import random


conn = sqlite3.connect("papalote.db")
cursor = conn.cursor()


"""Esto crea las tablas si no existen"""
def tablas():
    # bd de problemas
    cursor.execute("CREATE TABLE IF NOT EXISTS bd (id text, usuario text, fuente text, link text, solucion text, tex text)")
    conn.commit()

"""para iniciar la BD"""
def init():
    tablas()


"""*** Gestión de BD ***"""

"""obtenemos problamas por campo (estricto es para que sea justo ese)"""
def get(campo="", estricto=False):
    # obtenemos la tabla
    sql = "SELECT * FROM bd WHERE id "
    if estricto:
        sql += "= ?"
    else:
        sql += "LIKE ?"
        campo += "%"
    return [fila for fila in cursor.execute(sql, (campo,))]


"""agrega un problema"""
def add(campo, link, user="", font="", solution="", tex=""):
    # obtenemos el ID del problema en funcion del campo
    mismo_campo = [fila[0] for fila in get(campo)]  # solo el ID (0)

    # calculamos el indice (y el nombre)
    index = 0
    nombre = campo + str(index)
    while nombre in mismo_campo:
        index += 1
        nombre = campo + str(index)

    # agregamos el problema
    arr = [nombre, user, font, link, solution, tex]
    cursor.execute("INSERT INTO bd VALUES (?,?,?,?,?,?)", arr)
    conn.commit()
    return nombre


"""edita un problema de la BD"""
def edit(_id, nuevo_campo="", nuevo_link="", nuevo_user="", nueva_fuente="", nueva_sol="", nuevo_tex=""):
    problema = get(_id, True)
    if problema:
        # el problema existe, lo podemos cambiar
        # parseamos argumentos
        # id, usuario, fuente, link, solucion, tex
        args = list(problema[0])

        # los actualizamos si no estan vacíos
        args[1] = nuevo_user if nuevo_user else args[1]
        args[2] = nueva_fuente if nueva_fuente else args[2]
        args[3] = nuevo_link if nuevo_link else args[3]
        args[4] = nueva_sol if nueva_sol else args[4]
        args[5] = nuevo_tex if nuevo_tex else args[5]

        if nuevo_campo:
            # si queremos cambiar el campo, lo quitamos de la bd y lo volvemos a poner
            rm(_id)
            return add(nuevo_campo, args[3], args[1], args[2], args[4], args[5])
        else:
            cursor.execute("""UPDATE bd SET
            usuario = ?,
            fuente = ?,
            link = ?,
            solucion = ?,
            tex = ? WHERE id = ?""", tuple(args[1:] + [_id]))
            conn.commit()
            return _id
    else:
        return "No existe el problema *" + _id + "*"


"""Elimina un problema de la bd"""
def rm(nombre):
    cursor.execute(f"DELETE FROM bd WHERE id = ?", (nombre,))
    conn.commit()
    return cursor.rowcount


"""*** MÉTODOS UTILES PARA LA BD ***"""
def aleatorio(campo="", estricto=False, check_pdd=True):
    r = get(campo, estricto)
    # filtramos los que no esten en pdd
    if check_pdd:
        _pdd = [fila[0] for fila in cursor.execute("SELECT id FROM pdd WHERE fecha = ''")]
        r = [fila for fila in r if fila[0] not in _pdd]

    return random.choice(r) if r else []
