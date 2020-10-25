# AQUÍ VAN LOS COMANDOS de discord.py PARA LA BD

import bd.bd as b
import util
import argparse
import sys
from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    """añade un problema a la BD"""
    @commands.command()
    async def add(self, ctx, *args):
        # comprobamos permisos
        if not util.check_rol(ctx):
            await ctx.send("No tienes permisos para esta función")
            return

        if len(args) < 3:
            await ctx.send("Argumentos insuficientes")
            return

        # siempre será >add [campo]
        if args[0].startswith("-"):
            await ctx.send("ERROR: Asigna un campo a este problema (ej: '>add algebra ...')")
            return

        campo = args[0]
        args = args[1:]

        # comprobamos los posibles argumentos
        parse = argparse.ArgumentParser()
        parse.add_argument("-u", "--user", nargs='?', default=ctx.message.author.display_name)
        parse.add_argument("-f", "--font", nargs='?', default="Sin fuente")
        parse.add_argument("-l", "--link", default="")
        parse.add_argument("-L", "--LIST", default="")
        parse.add_argument("-s", "--solution", default="")
        parse.add_argument("-t", "--tex", nargs="*", default="")

        try:
            # probamos añadirlo
            r = parse.parse_args(args)
            output = b.add(campo, r.link, r.user, r.font, r.solution, " ".join(r.tex))
            await ctx.send(f'Nombre del archivo: *{output}*')
        except:
            await ctx.send("ERROR: Revisa que los argumentos sean correctos")


    """obtiene un problema"""
    @commands.command()
    async def get(self, ctx, *args):
        # opciones de la funcion autodescriptivas
        parse = argparse.ArgumentParser()
        parse.add_argument("--no-tex", dest="tex", action="store_false")
        parse.add_argument("--no-info", dest="info", action="store_false")
        #parse.add_argument("-s", "--strict", action="store_true")

        message, p = None, ""
        if len(args) == 0:
            # mostramos uno random
            p = b.aleatorio()
            message = await ctx.send(util.show_problem(p))
            if not util.check_rol(ctx): return

        else:
            # obtenemos el filtro (o problema concreto) y buscamos más argumentos
            nombre = False
            if not args[0].startswith('-'):
                nombre = args[0]
                args = args[1:]

        try:
            r = parse.parse_args(args)
            #p = b.aleatorio(nombre, r.strict) if nombre else b.aleatorio()
            strict = any(c.isdigit() for c in nombre)
            p = b.aleatorio(nombre, strict) if nombre else b.aleatorio()
            # si no se encuentran problemas
            if not p:
                await ctx.send("Sin resultados")
                return

            message = await ctx.send(util.show_problem(p, r.tex, r.info))
        except:
            print(sys.exc_info())


    @commands.command()
    async def show(self, ctx, *args):
        MAX = 15
        p = b.get() if not args else b.get(args[0])
        cuenta = len(p)
        p = [x[0] for x in p[:MAX]]  # limitamos a MAX, y cogemos solo el nombre
        await ctx.send(f"{cuenta} problemas:\n```\n" + "\n".join(p) + "\n```")


    @commands.command(name="del")
    async def _del(self, ctx, *args):
        if not util.check_rol(ctx):
            await ctx.send("Permiso denegado")

        if not args:
            await ctx.send("*del* necesita argumentos. (Ver >man del)")
            return

        # borramos cada archivo
        for x in args:
            b.rm(x)
           
        await ctx.send(f"Eliminados {len(args)} problemas")


    """editamos un problema"""
    @commands.command()
    async def edit(self, ctx, *args):
        # comprobamos permisos
        if not util.check_rol(ctx):
            await ctx.send("No tienes permisos para esta función")
            return

        if len(args) < 3:
            await ctx.send("Argumentos insuficientes")
            return

        if args[0].startswith("-"):
            await ctx.send("ERROR: Escribe el ID del problema a editar (ej: '>edit TDN3 ...')")
            return

        id_problema = args[0]
        args = args[1:]

        # comprobamos los posibles argumentos
        parse = argparse.ArgumentParser()
        parse.add_argument("-a", "--area", nargs='?', default="")
        parse.add_argument("-u", "--user", nargs='?', default=ctx.message.author.display_name)
        parse.add_argument("-f", "--font", nargs='?', default="Sin fuente")
        parse.add_argument("-l", "--link", default="")
        parse.add_argument("-L", "--LIST", default="")
        parse.add_argument("-s", "--solution", default="")
        parse.add_argument("-t", "--tex", nargs="*", default="")

        problema = b.get(id_problema, True)
        if not problema:
            await ctx.send(f"El problema {id_problema} no existe")
            return

        try:
            # probamos añadirlo
            r = parse.parse_args(args)

            output = b.edit(id_problema, r.area, r.link, r.user, r.font, r.solution, " ".join(r.tex))
            await ctx.send(f'Nombre del archivo: *{output}*')
        except:
            await ctx.send("ERROR: Revisa que los argumentos sean correctos")
