import discord
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
from googletrans import Translator
from youtube_search import YoutubeSearch
import youtube_dl
import os
from random import random, randrange
bot = commands.Bot(command_prefix = '!fm ')
bot.owner_id=5203

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
@bot.command()
async def ouija(ctx,*,pregunta):
    respuesta=["Probablemente","Todo apunta a que sí","Sin duda","Sí","Sí - definitivamente","Pregunta en otro momento","Será mejor que no te lo diga ahora","No cuentes con ello",
    "Mi respuesta es no",
    "Mis fuentes me dicen que no",
    "No",
    "No lo creo"]
    await ctx.send(random.choice(respuesta))
@bot.command()
async def ping(ctx):
    await ctx.send(round(bot.latency*1000))
@bot.command()
async def hora(ctx):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await ctx.send(current_time)


@bot.command()
async def join(ctx):
    channel= ctx.author.voice.channel
    voice=ctx.voice_client
    if voice is not None:
        return await voice.move_to(channel)
    await channel.connect()
@bot.command()
async def play(ctx, *,urlname: str):
    urlresult=YoutubeSearch(urlname, max_results=1).to_dict()
    print(urlresult)
    urlresult=urlresult[0]
    id,titulo = urlresult["id"],urlresult["title"]
    print(id,titulo)
    url="https://www.youtube.com/watch?v="+id
    print(url)
    channel= ctx.author.voice.channel
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        return

    await ctx.send("Cargando")

    voice=ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Descargando audio\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: terminada(ctx))
    await ctx.send(f"Ahora Tocando: {titulo}")
    print("Tocando\n")
async def terminada(ctx):
    await ctx.send("Cancion Terminada!")
@bot.command()
async def autor(ctx):
    await ctx.send("@"+str(bot.owner_id))
def calcularganador(board):
    boardtemplate=[
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]]
    for i in range(0,8):
        [a,b,c]=boardtemplate[i]
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return True
    return False

@bot.command()
async def gato(ctx):
    await ctx.send("MIAU")
    board=["  ","  ","  ","  ","  ","  ","  ","  ","  "]
    player=0
    mvments=[]
    await ctx.send("|----|----|----\n|----|----|----\n|----|----|----")
    winner=False
    while(winner==False):
        for i in range(0,9):
            if board[i] == "":
                mvments.append(i)
        await ctx.send(board[0]+board[1]+board[2]+"\n "+board[3]+board[4]+board[5]+"\n"+
        board[6]+board[7]+board[8]+"\n"+
        "\nLos movientos disponibles son" + str(mvments))
        response = await bot.wait_for('message')
        num = int(response.content)
        while(num not in mvments):
            await ctx.send("Opcion invalida")
            response = await bot.wait_for('message')
            num = int(response.content)
        if player==0:
            board[num]="0"
        else:
            board[num]="X"
        player=1
        mvments=[]
        winner=calcularganador(board)
        if len(mvments)==0:
            winner=True
            await ctx.send("Empate")
        
@bot.command()
async def traductor(ctx,lang,string):
    translator = Translator()
    k=translator.translate(string,dest=lang)
    await ctx.send(k.text)
@bot.command()

@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()
bot.run('NzI5ODcxMzIxMDcyMjcxMzgx.XwPP6g.x_VWQUGeTGSrlpZbPgWA9D8N2-s')
