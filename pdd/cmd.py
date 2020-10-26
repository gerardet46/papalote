# AQUÍ VAN LOS COMANDOS de discord.py PARA LA BD

import pdd.pdd as pd
import bd.bd as b
import variables as v
import util
import argparse
import sys
import random
import schedule
import asyncio
import datetime as dt
from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="pdd-add")
    async def pdd_add(self, ctx, *args):
        # check rols
        if not util.check_rol(ctx, ['admin', 'moderador', 'pdd selección']):
            await ctx.send("No tienes permisos para esta función")
            return

        if len(args) < 2:
            await ctx.send("Esta función necesita al menos 2 argumentos (>man pdd-add)")
            return

        if args[0] not in "fmd":  # facil-medio-dificil
            await ctx.send("El primer parámetro debe ser 'f', 'm' o 'd' (>man pdd-add)")
            return

        dif = args[0]
        args = list(args[1:])
        pd.add(args, dif)
        await ctx.send("Hecho!")


    @commands.command(name="pdd-get")
    async def pdd_get(self, ctx, *args):
        if not util.check_rol(ctx, ['admin', 'moderador', 'pdd selección']):
            await ctx.send("No tienes permisos para esta función")
            return

        nombre = ""
        if args: nombre = args[0]
        
        prob = pd.get(nombre)
        p = random.choice(prob)[0] if prob else []
        p_bd = b.get(p, True)
        
        if p_bd:
            await ctx.send(util.show_problem(p_bd[0]))
        else:
            await ctx.send("Este no existe en la BD")



    @commands.command(name="pdd-rm")
    async def pdd_rm(self, ctx, *args):
        # check rols
        if not util.check_rol(ctx, ['admin', 'moderador', 'pdd selección']):
            await ctx.send("No tienes permisos para esta función")
            return

        if args:
            pd.rm(list(args))
            await ctx.send("Hecho!")
        else:
            await ctx.send("No se han especificado problemas")


    @commands.command(name="pdd-list")
    async def pdd_list(self, ctx, *args):
        if '--old' in args:
            sql = "SELECT * FROM pdd WHERE fecha <> '' ORDER BY date(fecha) DESC"
            pd.cursor.execute(sql)
            r = pd.cursor.fetchall()
            l = len(r)
            r = r[:10]
            await ctx.send(f"{l} problemas archivados\n```\n" +
                           "\n".join([f"{x[0]}\t({x[2]})" for x in r]) + "```")
            return


        sql = "SELECT * FROM pdd WHERE fecha = ''"
        pd.cursor.execute(sql)
        r = pd.cursor.fetchall()

        if not r:
            await ctx.send("Sin resultados")
            return

        arr = [x[0] for x in r if x[1] == 'f']
        if arr:
            await ctx.send("Fácil:\n```\n" + "\n".join(arr) + "\n```")

        arr = [x[0] for x in r if x[1] == 'm']
        if arr:
            await ctx.send("Intermedio:\n```\n" + "\n".join(arr) + "\n```")

        arr = [x[0] for x in r if x[1] == 'd']
        if arr:
            await ctx.send("Difícil:\n```\n" + "\n".join(arr) + "\n```")

        pd.conn.commit()


    @commands.command(name="pdd-recover")
    async def recover(self, ctx, *args):
        if not util.check_rol(ctx):
            await ctx.send("No tienes permisos")
            return

        PDD()  # se asignará v.pdd_problema, y como la tarea() está en bucle, lo pondrá en el canal

        
"""Tarea del dia"""
async def tarea(bot):
    await bot.wait_until_ready()

    schedule.every().day.at('00:00').do(PDD)

    while True:
        schedule.run_pending()  # corremos las tareas pendientes
        if v.pdd_problema:
            # son las 00:00!!! => Mostrar PDD
            print(v.pdd_problema)

            f = open("pdd.log", "a")
            f.write(v.pdd_problema)
            f.close()

            canal = bot.get_channel(753290108995895296)
            message = await canal.send(v.pdd_problema)
            await message.add_reaction("\U0001F37E")
            #await canal.send("<@&765165103401271346>")  # avisamos
            v.pdd_problema = None

        await asyncio.sleep(20)


"""método para la tarea diaria"""
def PDD():
    p = pd.tarea_diaria()
    if p == "ERROR":
        v.pdd_problema = "No quedan problemas en PDD"
        return

    problema = b.get(p[0][0], True)[0]
    dif = {
        'f': 'fácil',
        'm': 'intermedio',
        'd': 'difícil'
    }
    v.pdd_problema = show_problem(problema, dif[p[0][1]], p[1])


"""lo mismo que util.py pero para el pdd"""
def show_problem(arr, dif, archivado):
    t = "**PROBLEMA DEL DÍA (" + str(dt.datetime.now().date()) + ')**\n'
    t += "*(Archivado)*\n" if archivado else "\n"

    t += "<@&765165103401271346>"
    t += "\n**Nombre**: " + arr[0]
    t += "\n**Fuente**: " + arr[2]
    t += "\n**Dificultad**: " + dif
    t += "\n**Propuesto por**: " + arr[1]
    t += "\n**Link**: " + arr[3]
    return t
