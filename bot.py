#!/usr/bin/env python3

import bd, pdd, man
import secrets
import variables as v
import datetime as dt
import schedule, asyncio
import discord
from discord.ext import commands


"""iniciamos el bot"""
# NOTE: Canviar es prefix quan acabi
prefix = "%"
bot = commands.Bot(command_prefix=prefix)


"""iniciamos el bot"""
@bot.event
async def on_ready():
    print("Bot listo!!")
    """# migración
    f = open("bdmigra.txt", "r")
    c = f.readlines()
    f.close()
    canal = bot.get_channel(751139496065630352)
    bd.bd.cursor.execute("DELETE FROM bd")
    bd.bd.conn.commit()
    for x in c:
        arr = x.split("|||")
        sol = arr[4] if arr[4] else ""
        bd.bd.add(arr[0], arr[3], arr[1], arr[2], sol)
    """



"""Notas de versión"""
@bot.command()
async def whatsnew(ctx):
    await ctx.send("""
**Papalote 2.0**

**Miembros**
```
Ahora puedes obtener un problema de manera más eficiente, usando >get para uno random, >get TDN para uno de TDN aleatorio, y ">get GEO21 --strict" para ese problema en específico

Los manuales han cambiado un poco la estructura. Haciendo >man está el manual principal, y >man add el manual para agregar, por ejemplo.
    Si el embed aparece en rojo, es que es el manual del comando, si es verde, como pdd, es un comando que contiene otros
```
**Admins**
```
La manera de manejar la bd es la misma, salvo las listas. Por ahora solo se puede poner pdd, que es una lista especial. Entra en *>man pdd* para más info
```
**Notas de la versión**
```
- Ahora usa SQLite3 para mayor comodidad.
- Separación de archivos para que sea más modular y escalable
- Los problemas del día se seleccionan para que cambien de dificultad y de campo
```""")


"""añadimos los comandos"""
bot.add_cog(bd.cmd.Cog(bot))
bot.add_cog(pdd.Cog(bot))
bot.add_cog(man.Cog(bot))


"""Problema del día"""


bot.loop.create_task(pdd.tarea(bot))


"""corremos el bot"""
bot.run(secrets.TOKEN)
