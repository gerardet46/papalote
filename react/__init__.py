import os
import json
import util
import discord
from discord.ext import commands

ARCHIVO = "react/reactions.json"
dicc = {}


"""cosas utiles"""
def guardar_json():
    f = open(ARCHIVO, 'w')
    f.write(json.dumps(dicc))
    f.close()


if not os.path.exists(ARCHIVO):
    guardar_json()


f = open(ARCHIVO, 'r')
dicc = json.loads(f.read())  # este es el diccionario
f.close()


async def on_react(user, payload, bot):
    msg_id = str(payload.message_id)
    emoji = payload.emoji.name
    guild = discord.utils.find(lambda x : x.id == payload.guild_id, bot.guilds)

    if msg_id in dicc:
        reacciones = dicc[msg_id]
        if emoji in reacciones:
            em, rol = reacciones[emoji], None
            if em.isdigit():
                rol = discord.utils.get(guild.roles, id=int(em))
            else:
                rol = discord.utils.get(guild.roles, name=em)

            await payload.member.add_roles(rol)
            await payload.member.send("Se te ha concedido el rol **" + reacciones[emoji] + "**")



async def on_anti_react(user, payload, bot):
    msg_id = str(payload.message_id)
    emoji = payload.emoji.name
    guild = discord.utils.find(lambda x : x.id == payload.guild_id, bot.guilds)

    if msg_id in dicc:
        reacciones = dicc[msg_id]
        if "add_only" in reacciones:
            return
       
        if emoji in reacciones:
            rol = discord.utils.get(guild.roles, name=reacciones[emoji])
            await user.remove_roles(rol)
            await user.send("Ya no tienes el rol **" + reacciones[emoji] + "**")



"""comandos del bot"""
class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="react-add")
    async def react_add(self, ctx, *args):
        if not util.check_rol(ctx):
            await ctx.send("No tienes permisos")
            return

        args = list(args)
        add_only = False # no permite quitarse el rol
        if "--add-only" in args:
            add_only = True
            args.remove("--add-only")

        l = len(args)
        if l > 2:
            _id = args[0]
            roles = {}
            for i in range(1, l, 2):
                if i + 1 < len(args):
                    if args[i + 1]:
                        roles[args[i]] = args[i + 1]
                else:
                    await ctx.send("Hay un emoji que queda sin rol. (>man react add)")
                    return

            if add_only:
                roles["add_only"] = True

            dicc[_id] = roles
            guardar_json()
            await ctx.send("Hecho!")
        else:
            await ctx.send("Argumentos insuficientes. (>man react add)")


    @commands.command(name="react-append")
    async def react_append(self, ctx, *args):
        if not util.check_rol(ctx):
            await ctx.send("No tienes permisos")
            return

        l = len(args)
        if l > 2:
            _id = args[0]
            roles = {}
            for i in range(1, l, 2):
                if i + 1 < len(args):
                    if args[i + 1]:
                        roles[args[i]] = args[i + 1]
                else:
                    await ctx.send("Hay un emoji que queda sin rol. (>man react append)")
                    return

            dicc[_id] = {**dicc[_id], **roles}  # agregamos
            guardar_json()
            await ctx.send("Hecho!")
        else:
            await ctx.send("Argumentos insuficientes. (>man react append)")


    @commands.command(name="react-list")
    async def react_list(self, ctx, *args):
        if not util.check_rol(ctx):
            await ctx.send("No tienes permisos")
            return

        info = True
        args = list(args)
        if "--no-info" in args:
            args.remove("--no-info")
            info = False

        if args:
            _id = args[0]
            if _id in dicc:
                await ctx.send(f"Reacciones para {_id}\n" + "\n".join([f"{k}\t{dicc[_id][k]}" for k in dicc[_id]]))
            else:
                await ctx.send(f"No hay reacciones para el mensage *{_id}*")

        elif dicc:
            msg = []
            for k in dicc:
                if info:
                    msg.append(f"Reacciones para *{k}*\n" + "\n".join([f"{_k}\t{dicc[k][_k]}" for _k in dicc[k]]))
                else:
                    msg.append(k)

            await ctx.send("\n\n".join(msg))
        else:
            await ctx.send("No se ha configurado ningún \"reaction role\"")


    @commands.command(name="react-rm")
    async def react_rm(self, ctx, *args):
        if not util.check_rol(ctx):
            await ctx.send("No tienes permisos")
            return

        if args:
            for x in args:
                if x in dicc:
                    del dicc[x]

            guardar_json()
            await ctx.send("Hecho!")
        else:
            await ctx.send("Esta función necesita argumentos (>man react rm)")
