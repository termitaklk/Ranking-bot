import discord
import requests
import asyncio
import schedule
import datetime
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")
DISCORD_POST_CHANNEL_ID=os.getenv("DISCORD_POST_CHANNEL_ID")
DISCORD_CONGRATS_CHANNEL_ID=os.getenv("DISCORD_CONGRATS_CHANNEL_ID")
API_URL=os.getenv("API_URL")
TIME_EXECUTION=int(os.getenv("TIME_EXECUTION"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def obtener_info_tabla():
    try:
        respuesta = requests.get(API_URL)
        data = respuesta.json()

        leaderboard_info = "" * 5
        leaderboard_info += f"{'Position':<10}{'Player':<14}{'Score':<8}{'🔼  🔽 '}\n"
        leaderboard_info += "" * 5 + "\n"

        if isinstance(data, dict) and "data" in data:
            data_list = data["data"]
            for item in data_list:
                if isinstance(item, dict):
                    player = f"{item.get('value', 'Desconocido')}"
                    position = str(item.get("position", "Desconocida")).center(8)
                    score = str(item.get("score", 0)).center(10)
                    difference_value = item.get('difference', 0)
                    
                    if difference_value > 0:
                        difference = f"🔼 ({difference_value})  ".center(6)


                    elif difference_value < 0:
                        difference = f"🔻 ({difference_value}) ".center(6)

                    else:
                        difference = "❓".center(8)

                    leaderboard_info += f"{position:<9}{player:<13}{score:<10}{difference}\n"

            leaderboard_info += "" * 10

            if ultima_ejecucion:
                ultima_ejecucion_str = ultima_ejecucion.strftime("%Y-%m-%d %H:%M:%S")
                last_updated = f"Last updated on: {ultima_ejecucion_str}"
                centralizado = last_updated.center(40)
                leaderboard_info += f"{centralizado}\n"

            return "`" + leaderboard_info + "`"

    except Exception as e:
        print(f"Error al obtener la información: {e}")
        return None



info_message = None
ultima_ejecucion = None

async def enviar_info_al_canal(info):
    global info_message

    canal = bot.get_channel(int(DISCORD_POST_CHANNEL_ID))
    if not canal:
        print(f"No se pudo encontrar el canal con el ID {DISCORD_POST_CHANNEL_ID}.")
        return

    embed = discord.Embed(title="Ranking Evolution!!", description=info, color=0x000000)  # Color negro

    if not info_message:
        info_message = await canal.send(embed=embed)
    else:
        await info_message.edit(embed=embed)

    print(info)



def ejecutar_tarea():
    global ultima_ejecucion
    ultima_ejecucion = datetime.datetime.now()
    info_tabla = obtener_info_tabla()
    asyncio.ensure_future(enviar_info_al_canal(info_tabla))

schedule.every(TIME_EXECUTION).minutes.do(ejecutar_tarea)

async def imprimir_tiempo_restante():
    while True:
        next_run = schedule.next_run()
        tiempo_restante = next_run - datetime.datetime.now()
        ultima_ejecucion_str = ultima_ejecucion.strftime("%Y-%m-%d %H:%M:%S") if ultima_ejecucion else "N/A"
        print(f"Próxima ejecución en: {tiempo_restante}, Última ejecución: {ultima_ejecucion_str}")
        await asyncio.sleep(60)

async def ejecutar_programa():
    loop.create_task(imprimir_tiempo_restante())
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

@bot.event
async def on_ready():
    try:
        print(f"Conectado como {bot.user.name}")
        await enviar_info_al_canal(obtener_info_tabla())
    except Exception as e:
        print(f"Error en on_ready: {e}")

loop = asyncio.get_event_loop()
loop.create_task(bot.start(DISCORD_TOKEN))
loop.create_task(ejecutar_programa())

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(bot.close())
finally:
    loop.close()















