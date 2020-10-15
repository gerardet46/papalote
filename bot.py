#!/usr/bin/env python3

import bd
import secrets
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


"""añadimos los comandos"""
bot.add_cog(bd.cmd.Cog(bot))


"""corremos el bot"""
bot.run(secrets.TOKEN)
