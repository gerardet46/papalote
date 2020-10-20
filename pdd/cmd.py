# AQUÍ VAN LOS COMANDOS de discord.py PARA LA BD

import pdd.pdd as pd
import bd.bd as b
import variables as v
import util
import argparse
import sys
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

        tarea(self.bot)
        """
        p = pd.tarea_diaria()
        if p == "ERROR":
            await ctx.send("No quedan problemas en PDD")
            return
       
        problema = b.get(p[0][0], True)[0]
        dif = {
            'f': 'fácil',
            'm': 'intermedio',
            'd': 'difícil'
        }
        msg = "**PROBLEMA DEL DÍA (" + str(dt.datetime.now().date()) + ')**\n'
        msg += "*(Archivado)*\n" if p[1] else ""
        msg += "**Dificultad:** " + dif[p[0][1]] + '\n\n'

        msg += util.show_problem(problema, False, True)
        await ctx.send(msg)
        """

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
            message = await canal.send(v.resultado)
            await message.add_reaction("\U0001F37E")
            await canal.send("<@&765165103401271346>")  # avisamos
            v.pdd_problema = None

        await asyncio.sleep(20)


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
    msg = "**PROBLEMA DEL DÍA (" + str(dt.datetime.now().date()) + ')**\n'
    msg += "*(Archivado)*\n" if p[1] else ""
    msg += "**Dificultad:** " + dif[p[0][1]] + '\n\n'

    msg += util.show_problem(problema, False, True)
    v.pdd_problema = msg
