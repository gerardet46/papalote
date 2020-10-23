import sqlite3
import random
import datetime as dt


conn = sqlite3.connect("papalote.db")
cursor = conn.cursor()


"""Esto crea las tablas si no existen"""
def tablas():
    # tabla del pdd
    cursor.execute("CREATE TABLE IF NOT EXISTS pdd (id text, dificultad text, fecha text)")
    conn.commit()


def init():
    tablas()


"""*** Gestión de PDD ***"""
def get(filtro="", estricto=False):
    if filtro:
        sql = f"SELECT * FROM pdd WHERE id "
        if estricto:
            sql += "= ?"
        else:
            sql += "LIKE ?"
            filtro += "%"

        return [fila for fila in cursor.execute(sql, (filtro,))]
    else:
        return [fila for fila in cursor.execute("SELECT * FROM pdd")]


def add(ids: list, dificultad):
    tabla, insertar = [x[0] for x in get()], []
    sql = "INSERT INTO pdd VALUES (?,?,?)"
    for x in ids:
        if x in tabla:
            rm([x])  # eliminamos para volverlo a agregar

        # agregamos
        insertar.append((x, dificultad, ''))

    cursor.executemany(sql, insertar)
    conn.commit()


def rm(ids: list):
    _ids = [(x,) for x in ids]
    sql = "DELETE FROM pdd WHERE id = ?"
    cursor.executemany(sql, _ids)
    conn.commit()


def aleatorio(filtro=""):
    r = get(filtro)
    return random.choice(r) if r else []


def tarea_diaria():
    compr_dias, archivado = 2, False
    cursor.execute("SELECT * FROM pdd ORDER BY date(fecha) DESC LIMIT " + str(compr_dias))
    r = cursor.fetchall()
    conn.commit()

    def quitar_numeros(s):
        return ''.join([c for c in s if not c.isdigit()]) + '%'

    # primero comprobamos si podemos evitar las 2 condiciones
    dif = r[0][1] + r[1][1]  # fm, fd, md, ...
    campos = [quitar_numeros(r[0][0]), quitar_numeros(r[1][0])]

    # filtramos
    cursor.execute("SELECT * FROM pdd WHERE fecha = '' AND id NOT LIKE ? AND id NOT LIKE ? AND dificultad <> ? AND dificultad <> ?",
                   (campos[0], campos[1], dif[0], dif[1]))
    filtro = cursor.fetchall()
    conn.commit()

    if not filtro:
        # buscamos solo un filtro
        cursor.execute("SELECT * FROM pdd WHERE fecha = '' AND id NOT LIKE ? AND dificultad <> ?",
                       (campos[0], dif[0]))
        filtro = cursor.fetchall()
        conn.commit()
        if not filtro:
            # buscamos solo un filtro
            cursor.execute("SELECT * FROM pdd WHERE fecha = '' AND id NOT LIKE ? AND dificultad <> ?",
                           (campos[1], dif[1]))
            filtro = cursor.fetchall()
            conn.commit()
            if not filtro:
                # sin filtro
                cursor.execute("SELECT * FROM pdd WHERE fecha = ''")
                filtro = cursor.fetchall()
                conn.commit()
                if not filtro:
                    cursor.execute("SELECT * FROM pdd")
                    filtro = cursor.fetchall()
                    conn.commit()
                    archivado = True

    if not filtro:
        return "ERROR"

    item = random.choice(filtro)

    # si no existe
    cursor.execute("SELECT * FROM bd WHERE id = ?", (item[0],))
    r = cursor.fetchall()
    if not r:
        cursor.execute("DELETE FROM pdd WHERE id = ?", (item[0],))
        conn.commit()
        return tarea_diaria()

    # si está archivado
    if not archivado:
        # pasamos a OLD
        cursor.execute("UPDATE pdd SET fecha = ? WHERE id = ?", (str(dt.datetime.now().date()), item[0]))
        conn.commit()
   
    return (item, archivado)
