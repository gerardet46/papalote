#!/usr/bin/env python3

import bd, pdd, man
import react

import secrets
import variables as v
import datetime as dt
import schedule, asyncio
import discord
from discord.ext import commands


"""iniciamos el bot"""
prefix = ">"
bot = commands.Bot(command_prefix=prefix)


"""iniciamos el bot"""
@bot.event
async def on_ready():
    print("Bot listo!!")


"""añadimos los comandos"""
bot.add_cog(bd.cmd.Cog(bot))
bot.add_cog(pdd.Cog(bot))
bot.add_cog(man.Cog(bot))
bot.add_cog(react.Cog(bot))


"""reacciones"""
@bot.event
async def on_raw_reaction_add(payload):
    user = discord.utils.get(bot.get_all_members(), id=payload.user_id)
    await react.on_react(user, payload, bot)


@bot.event
async def on_raw_reaction_remove(payload):
    user = discord.utils.get(bot.get_all_members(), id=payload.user_id)
    await react.on_anti_react(user, payload, bot)


"""Problema del día"""
bot.loop.create_task(pdd.tarea(bot))


"""corremos el bot"""
bot.run(secrets.TOKEN)
