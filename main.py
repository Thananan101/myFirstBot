import discord
import os 
from random import randrange
from replit import db
from keep_awake import keep_alive
from discord.ext import commands

from discord import FFmpegPCMAudio
from discord.utils import get
import youtube_dl

TOKEN = ('ODQ5OTg3ODM5Mjc3NzkzMjgw.YLjK3A.AA6ZPnjXHXUe4k0x_oiYNqnqq4Y')

client = commands.Bot(command_prefix = '$')

bPuen = ["ไอ่ปืนมันไก่กรู๊กกก", "น้องเกิ๊นน", "กระจอก", "ขี้เมา", "เด็กเหี้ย"]
bLung = ["ไอ้สัสลุง หัดใช้สมองบ้างนะไอ้เหี้ยย", "7 ปีละนะไอ้สัส เมื่อไหร่จะย้ายออกจากข้างบ้านกุซักที"]


@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))



@client.command(pass_context = True, aliases=["j"])
async def join(ctx):
  if (ctx.author.voice):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send("เข้ามาแล้วขอรับนายท่าน มีอะไรให้รับใช้")
  else:
    await ctx.message.channel.send("เข้าซักห้องก่อนค่อยเรียกกู ไอ่ฟาย")


@client.command(pass_context = True, aliases=["l"])
async def leave(ctx):
  if (ctx.voice_client):
    await ctx.voice_client.disconnect()
    await ctx.send("ไปละ บัยยย")
  else:
    await ctx.send("ไม่ กูไม่ออก ออกแล้วจะเอาอะไรแดก")

@client.command(pass_context = True, aliases=["ปิง"])
async def ping(ctx):
  await ctx.message.channel.send("Pong")

@client.command(pass_context = True)
async def roll(ctx):
  await ctx.message.channel.send(ctx.author.mention + "  " + str(randrange(100)))

@client.command(pass_context = True, aliases=["หยิ่ง"])
async def arrogant(ctx):
  await ctx.message.channel.send("จริง ในดิสมีแต่คนหยิ่ง หยิ่งเกิ๊นนนน")

@client.command(pass_context = True, aliases=["เอ้ว"])
async def elf(ctx):
  await ctx.message.channel.send("Jett korean อะ seoldam แต่น้องเอ้วอะ so hot")

# how to use custom emoji: <:emojiName:emojiID> you can get the id from sticker URL
@client.command(pass_context = True, aliases=["ปืน"])
async def puen(ctx):
  await ctx.message.channel.send(bPuen[randrange(len(bPuen))] + " <:kwy:844178327925424138>  <:puenKuan:841398727641137152>")

@client.command(pass_context = True, aliases=["ลุง"])
async def lung(ctx):
  await ctx.message.channel.send(bLung[randrange(len(bLung))] + " :footprints:")


@client.command(pass_context = True, aliases=["p", "pl"])
async def play(ctx, url:str):
  channel = ctx.author.voice.channel
  voice_client = get(client.voice_clients, guild=ctx.guild)

  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

  if not voice_client.is_playing():
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      URL = info['formats'][0]['url']
    voice_client.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    voice_client.is_playing()
  else:
    await ctx.message.channel.send("ร้องเพลงอยู่ไอ้สัส ไม่ว่างโว้ยยย")
    return






keep_alive()

client.run(TOKEN)