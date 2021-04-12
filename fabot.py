import discord
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
from googletrans import Translator
import os
import youtube_dl
import asyncio
import random as rand
import key
bot = commands.Bot(command_prefix = '!fm ')
bot.owner_id=5203
YDL_OPTIONS = {'format': 'bestaudio', 'default_search': 'ytsearch','outtmpl': 'songs/song.mp3', 'noplaylist':'True'}
@bot.event
async def on_ready():
	print('Logeado como {0.user}'.format(bot))
	channel = bot.get_channel(583432066234843207)
	await channel.send('FernandoBOT esta ONLINE')
@bot.command()
async def invocar(ctx):
    await ctx.send("He sido invocado")
@bot.command()
async def roll(ctx):
    await ctx.send(randrange(100))
#Elige una respuesta aleatoria, TODO: enviar un mensaje personalizado a partir de la pregunta
@bot.command()
async def ouija(ctx,*,pregunta):
    respuesta=["Probablemente","Todo apunta a que sí","Sin duda","Sí","Sí - definitivamente","Pregunta en otro momento","Será mejor que no te lo diga ahora","No cuentes con ello",
    "Mi respuesta es no",
    "Mis fuentes me dicen que no",
    "No",
    "No lo creo"]
    await ctx.send(rand.choice(respuesta))
@bot.command()
async def ping(ctx):
    await ctx.send(round(bot.latency*1000))
@bot.command()
async def hora(ctx):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await ctx.send(current_time)

#Entra al canal de voz TODO: hacer que play haga esto
@bot.command()
async def join(ctx):
    print("called")   
    channel= ctx.author.voice.channel
    voice=ctx.voice_client
    if voice is not None:
        return await voice.move_to(channel)
    await channel.connect()
#Para la reproduccion de audio
@bot.command()
async def stop(ctx):
        voice=ctx.voice_client
        if voice.is_playing():
                voice.stop()
#Pausa el audio
@bot.command()
async def pause(ctx):
        voice=ctx.voice_client
        if voice.is_playing():
                voice.pause()
@bot.command()
async def resume(ctx):
        voice=ctx.voice_client
        if voice.is_paused():
                voice.resume()
#Busca y descarga audio desde un video en youtube
@bot.command()
async def play(ctx,*,name):
    await ctx.send("Cargando")
    voice=ctx.voice_client
    if voice.is_playing():
            ctx.send("Espera a que termine la cancion!")
            return
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(name, download=False)
            entries= info.get('entries')[0]
            title=entries.get('title')
            ydl.download([name])
            await ctx.send("Ahora tocando: " + title)
    voice.play(discord.FFmpegPCMAudio('songs/song.mp3'),after=terminada)
    print("Tocando\n")
@bot.command()
async def op(ctx):
    channel= ctx.author.voice.channel
    await ctx.send("Cargando")
    voice=ctx.voice_client
    if voice is None:
        await channel.connect()
        voice=ctx.voice_client
    directory=f'canciones/{randrange(18)}.mp3'
    isplaying=True
    voice.play(discord.FFmpegPCMAudio(directory),after= terminada)
    print("Tocando\n")
@bot.command()
async def oploop(ctx):
    channel= ctx.author.voice.channel
    await ctx.send("Cargando")
    voice=ctx.voice_client
    if voice is None:
        await channel.connect()
        voice=ctx.voice_client
    canciones=list(range(1, 19))
    print(canciones)
    while(len(canciones)!=0):
            print(canciones)
            randomN=rand.choice(canciones)
            directory=f'canciones/{randomN}.mp3'
            isplaying=True
            canciones.remove(randomN)
            voice.play(discord.FFmpegPCMAudio(directory))
            await asyncio.sleep(106)
    print("Terminado\n")
#Envia un mensaje al chat, TODO: enviar al canal correspondiente de ka fuente de audio
def terminada(err):
        channel=bot.get_channel(728396177048993833)
        coro=channel.send("Ok!")
        fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
        os.remove("songs/song.mp3")
        try:
                fut.result()
        except:
                print("Sadge" + err)
                pass
@bot.command()
async def autor(ctx):
    await ctx.send("@"+str(bot.owner_id))
#dado lenguaje y texto traduce el texto al lenguaje del inputs
@bot.command()
async def traductor(ctx,lang,string):
    translator = Translator()
    k=translator.translate(string,dest=lang)
    await ctx.send(k.text)
@bot.command()
#"Apagar" bot
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()
bot.run(key.token)
