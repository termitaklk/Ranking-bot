import discord
import requests
import json
import asyncio

# Token del bot de Discord
TOKEN = "MTEzOTk4NjU5NTY0NzMyODI2OA.GMXNeN.C0zPgmRXJDoYQaTb7TB_kYGVMujZJgaLur6SX4"

# URL a la que se realizará la petición GET
URL = "https://evolutionygo.com/api/leaderboard"

# ID del canal donde se enviará la información del Ranking
CANAL_ID = "1138104595315433603"

# ID del canal donde se enviará el mensaje cuando un Jugador suba 2 posiciones o mas.
CANAL_SUBIDA_ID = "1138104595315433603"

# Intents Requeridos en Discord.
intents = discord.Intents.default()
intents.message_content = True

# Crear una instancia del cliente de Discord con los intents
cliente = discord.Client(intents=intents)

# Variable para guardar el mensaje enviado al canal
mensaje_en_canal = None

# Diccionario para almacenar la última posición de cada jugador
ultima_info_tabla = {}


# Función para obtener la información de la tabla de clasificación
def obtener_info_tabla():
    try:
        # Realizar la petición GET a la URL
        respuesta = requests.get(URL)
        data = respuesta.json()

        leaderboard_info = f"Position | Username | Points\n```md\n"
        jugadores_actuales = {}

        for i, item in enumerate(data):
            if i >= 20:
                break

            player = item["value"]
            score = item["score"]
            jugadores_actuales[player] = i + 1

            cambio = ""
            posicion_anterior = ultima_info_tabla.get(player)
            if posicion_anterior is not None:
                diferencia_posicion = posicion_anterior - (i + 1)
                if diferencia_posicion > 0:
                    cambio = f"⬆️ (+{diferencia_posicion})"  # Jugador subió
                    # Si el jugador sube dos o más posiciones, enviar mensaje al canal especificado
                    if diferencia_posicion >= 2:
                        asyncio.create_task(
                            enviar_mensaje_subida(player, diferencia_posicion)
                        )
                elif diferencia_posicion < 0:
                    cambio = f"⬇️ (-{abs(diferencia_posicion)})"  # Jugador bajó
                ultima_info_tabla[player] = i + 1

            leaderboard_info += f"{i+1} | {player} | {score} {cambio}\n"

        leaderboard_info += "```"

        return leaderboard_info, jugadores_actuales

    except Exception as e:
        print(f"Error al obtener la información: {e}")
        return None, {}


# Función para enviar el mensaje al canal cuando un jugador sube dos o más posiciones
async def enviar_mensaje_subida(player, diferencia_posicion):
    canal_subida = cliente.get_channel(int(CANAL_SUBIDA_ID))
    if canal_subida:
        await canal_subida.send(
            f"¡{player} subió {diferencia_posicion} posiciones en la clasificación del Ranking!"
        )


# Función para enviar o actualizar la información de la tabla de clasificación en el canal
async def enviar_info_al_canal(info):
    global mensaje_en_canal
    canal = cliente.get_channel(int(CANAL_ID))
    if canal is None:
        print(
            f"No se pudo encontrar el canal con el ID {CANAL_ID}. Verifica que el bot tenga acceso al canal y el ID sea correcto."
        )
        return

    if mensaje_en_canal:
        await mensaje_en_canal.edit(
            content=info
        )  # Actualizar el mensaje existente en el canal
    else:
        mensaje_en_canal = await canal.send(info)  # Enviar un nuevo mensaje al canal


# Evento que se ejecuta cuando el bot se conecta correctamente
@cliente.event
async def on_ready():
    print(f"Conectado como {cliente.user.name}")
    await verificar_info_tabla()  # Cargar y enviar la información de la tabla de clasificación al inicio


# Función para verificar la tabla de clasificación y enviarla al canal
async def verificar_info_tabla():
    global ultima_info_tabla
    while True:
        info_tabla, nuevas_posiciones = obtener_info_tabla()

        # Imprimir la clasificación actual
        print("Clasificación actual:")
        print(info_tabla)

        # Si hay cambios en la clasificación, enviar la información al canal
        if ultima_info_tabla != info_tabla:
        # if nuevas_posiciones:
            ultima_info_tabla = nuevas_posiciones.copy()
            await enviar_info_al_canal(info_tabla)
        await asyncio.sleep(600)  # Esperar 10 minutos


# Comando para realizar la petición GET y mostrar la información en el canal específico
@cliente.event
async def on_message(mensaje):
    if mensaje.content.startswith("!obtener_info"):
        try:
            info_tabla, _ = obtener_info_tabla()
            await enviar_info_al_canal(info_tabla)
        except Exception as e:
            await mensaje.channel.send(f"Error al enviar la información: {e}")


# Ejecutar el bot
cliente.run(TOKEN)
