# incluimos todos los módulos del paquete

import json
import discord
from discord.ext import commands

# manual: tuple, list
def get_man(manual):
    dicc = MANUAL
    if manual:
        # navegamos entre las claves
        for x in manual:
            if x in dicc:
                dicc = dicc[x]
            else:
                return dicc  # error

    return dicc


# discord
class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def man(self, ctx, *args):
        manual = get_man(args)
        if isinstance(manual, dict):
            # ayuda general
            keys = list(manual.keys())

            embed = discord.Embed(description = "Ver >man " + " ".join(args) + " [cmd]", color = discord.Color.green())
            embed.set_author(name = " -> ".join(args))
            embed.set_thumbnail(url = "https://media.discordapp.net/attachments/741478537382330378/759424400318791721/20200804_220902.png")

            embed.add_field(name = "Comandos", value = "\n".join(keys))
            await ctx.send(embed = embed)
        else:
            # [entrada, {cosas}]
            embed = discord.Embed(description = manual[0], color = discord.Color.red())
            embed.set_author(name = " -> ".join(args))
            embed.set_thumbnail(url = "https://media.discordapp.net/attachments/741478537382330378/759424400318791721/20200804_220902.png")

            if isinstance(manual[-1], dict):
                for k, j in manual[-1].items():
                    embed.add_field(name = k, value = j, inline = False)

            await ctx.send(embed = embed)


MANUAL = {
    "add": [
        "Agregar problemas. Esta función añade un problema a la BD y devuelve un identificador, por ejemplo, *algebra12*. Esto es para poder editar el problema, obtenerlo y agregarlo a listas",
        {
            "Uso": ">add [campo] [ARGUMENTOS]",
            "Argumentos": "\n".join([
                "-f, --fuente: fuente del problema",
                "-u, --user: usuario",
                "-l, --link: link",
                "-L, --LIST: de paso los agraga a unas listas (separadas por coma)",
                "-s, --solution: link a la solución",
                "-t, --tex (siempre al final): tex",
                "el campo al principio y todos son opcionales menos el link y el campo"
            ]),
            "Ejemplos": "\n\n".join([
                ">add algebra -f IMO98 -l http://google.com -t \\textbf{CONTENIDO TEX}",
                ">add TDN -u gerardet46 -f \"Fuente con espacio\" -l LINK_OBLIGATORIO",
                ">add TDN -L IMO,PDD,OME --solution http:... -l ... --tex contenido latex aquí"
            ])
        }
    ],
    "edit": [
        "Editar problemas. Esta función añade un problema a la BD y devuelve un identificador, por ejemplo, *algebra12*. Esto es para poder editar el problema, obtenerlo y agregarlo a listas",
        {
            "Uso": ">edit [id_problema] [ARGUMENTOS]",
            "Argumentos": "\n".join([
                "-a, --area: cambia el campo del problema",
                "-f, --fuente: fuente del problema",
                "-u, --user: usuario",
                "-l, --link: link",
                "-s, --solution: link a la solución",
                "-t, --tex (siempre al final): tex",
                "TODOS son opcionales. Si no se ponen, se mantienen el resto de valores"
            ]),
            "Ejemplos": "\n\n".join([
                ">edit algebra0 -f IMO98 -l http://google.com -t \\textbf{CONTENIDO TEX}",
                ">edit TDN0 -u gerardet46 --area álgebra"
            ])
        }
    ],
    "del": [
        "Esto es para eliminar problemas de la bd",
        {"Argumentos": "...", }
    ],
    "get": [
        "Muestra un problema (concreto o random)",
        {"Argumentos": "OPCIONALES\nNombre del problema o campo\n--no-info: solo muestra la imagen del problema, sin la info\n" \
         "-s, --strict: Devuelve el problema dado estrictamente (>get TDN1 puede devolver TDN1, TDN12, TDN134, ..., pero con -s, --strict no)\nno-tex: muestra todo menos el LaTex",
         "Ejemplos": "\n".join([
             ">get (uno random)",
             ">get algebra (uno random de algebra)",
             ">get albegra0 (muestra el problema algebra0)",
             ">get algebra --no-info -s (random de algebra sin info y estricto)",
             ">get --no-tex (random sin mostrar el latex)"
         ]),
         "Extra": "El bot reacciona con un emoji cada problema, si el usuario que usó el comando también lo reacciona, el bot le mandará un dm con las pistas del problema (si es que hay). Si vuelve a reaccionar al mensaje privado, el bot lo editará por la solución del problema (en caso de que esté registrada).",}
    ],
    "show": [
        "Para mostrar el nombre de los archivos disponibles.",
        {"Argumentos": "ES OPCIONAL\nInluir un patrón de búsqueda tal como un campo",
         "Ejemplos": "\n".join([">show", ">show algebra"])}
    ],
    "pdd": {
            "add": ["(pdd-add) Agrega al PDD", {
                "Sintaxis": ">man [dificultad] [problema1] [problema2] ...",
                "Parámetros": "[dificultad]: f|m|d, según si es Fácil, interMedio o Difícil",
                "Ejemplos": ">pdd-add f TDN2 COM0\n>pdd-add d GEO1"
            }],
            "rm": ["(pdd-rm) Elimina problemas del PDD", {"Sintaxis": "%pdd-rm [problema1] [problema2] ..."}],
            "list": ["(pdd-list) Muestra los problemas de PDD", {
                "Argumentos": "--old: muestra los problemas que ya salieron",
                "Ejemplos": ">pdd-list\n>pdd-list --old"
            }],
            "recover": ["(pdd-recover) (SOLO EN CASO DE ERRORES)\nSi falla el problema del día, haciendo esto se hará manualmente.", {"Uso": ">pdd-recover"}]
    },
    "l-add": [
        "Agrega problemas a listas (o baterías de problemas)",
        {
            "Argumentos": ">l-add {lista1} {lista2} {...} -p {problema1} {problema2} {...}" \
            "\nEsto agrega los problemas *problema1*, *p2*, ... a las listas *lista1*, *lista2*, ..."
        }
    ],
    "l-count": [
        "Cuenta cúantos problemas hay en las listas",
        {
            "Argumentos": "(OPCIONALES): [lista1] [lista2] ...",
            "Ejemplos": "\n".join([
                "**>l-count** -> devuelve cuántos problemas tiene cada lista (todas)",
                "**>l-count IMO PDD** -> solo cuenta las listas *PDD* y *IMO*"
            ])
        }
    ],
    "l-rm": [
        "Elimina problemas en las listas",
        {
            "Argumentos": ">l-rm {lista1} {lista2} {...} -p {problema1} {problema2} {...}" \
            "\nEsto elimina los problemas *problema1*, *p2*, ... de las listas *lista1*, *lista2*, ..."
        }
    ],
}
