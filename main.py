import discord
import os 
from random import randrange
from replit import db
from keep_awake import keep_alive
from discord.ext import commands

from discord import FFmpegPCMAudio
from discord.utils import get
import youtube_dl
from alarm import *

from datetime import datetime   #To set date and time

from os import system

TOKEN = ('ODQ5OTg3ODM5Mjc3NzkzMjgw.YLjK3A.AA6ZPnjXHXUe4k0x_oiYNqnqq4Y')

client = commands.Bot(command_prefix = '$')

bPuen = ["ไอ่ปืนมันไก่กรู๊กกก", "น้องเกิ๊นน", "กระจอก", "ขี้เมา", "เด็กเหี้ย"]
bLung = ["ไอ้สัสลุง หัดใช้สมองบ้างนะไอ้เหี้ยย", "7 ปีละนะไอ้สัส เมื่อไหร่จะย้ายออกจากข้างบ้านกุซักที"]
bTee = ["ไม่มีคอนโดมาเอากับพี่ <:Tee_smile:850487711420645386>", "ผมไม่ใช่ทีธรรมดา ผมอะทีรัก <:Tee_smile:850487711420645386>"]

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))



@client.command(pass_context = True, aliases=["j"])
async def join(ctx):
  voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice_client == None:
    if (ctx.author.voice):
      channel = ctx.author.voice.channel
      await channel.connect()
      await ctx.send("เข้ามาแล้วขอรับนายท่าน มีอะไรให้รับใช้")
    else:
      await ctx.message.channel.send("เข้าซักห้องก่อนค่อยเรียกกู ไอ่ฟาย")
  


@client.command(pass_context = True, aliases=["l", "dc"])
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
  await ctx.message.channel.send("Jett korean อะ seoldam แต่น้องเอ้วอะ so hot   <:sohuttt:850139344836886568>")

# how to use custom emoji: <:emojiName:emojiID> you can get the id from sticker URL
@client.command(pass_context = True, aliases=["ปืน"])
async def puen(ctx):
  await ctx.message.channel.send(bPuen[randrange(len(bPuen))] + " <:kwy:844178327925424138>  <:puenKuan:841398727641137152>")

@client.command(pass_context = True, aliases=["ลุง"])
async def lung(ctx):
  await ctx.message.channel.send(bLung[randrange(len(bLung))] + " :footprints:")

@client.command(pass_context = True, aliases=["เท็น"])
async def ten(ctx):
  await ctx.message.channel.send("เหล่ท่อ <:tenenz:841397333136244756>")

@client.command(pass_context = True, aliases=["ชานม", "หนม", "น้ำหวาน", "ขนมนมเนยนุ๊บนิ๊บ"])
async def chanom(ctx):
  await ctx.message.channel.send("ไอ้นั่นมันชื่อภูมิ ไอ้สัส เรียกให้ถูกดิ๊ <:Chandsome:851074765305020476>")

@client.command(pass_context = True, aliases=["ภูมิ"])
async def poom(ctx):
  await ctx.message.channel.send("สวัสดีคร้าบบ ทุกคนนน ผมชื่อภูมินะครับ <:Chandsome:851074765305020476>")

@client.command(pass_context = True, aliases=["ที"])
async def tee(ctx):
  await ctx.message.channel.send(bTee[randrange(len(bTee))])

@client.command(pass_context = True, aliases=["p", "pl"])
async def play(ctx, url:str):

  voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice_client == None:
    if (ctx.author.voice):
      channel = ctx.author.voice.channel
      await channel.connect()
      await ctx.send("เข้ามาแล้วขอรับนายท่าน มีอะไรให้รับใช้")
    else:
      await ctx.message.channel.send("เข้าซักห้องก่อนค่อยเรียกกู ไอ่ฟาย")
    
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

#บอทเข้าห้องไม่ได้ติด channel.connect()

@client.command(pass_context = True)
async def alarm(ctx, alarm_time):
  fk_time = alarm_time
  validate = validate_time(alarm_time)
  alarm_time = timezoneToTH(alarm_time)
  print(alarm_time)
  print(validate)
  print(len(alarm_time))
  if validate != "ok":
    await ctx.message.channel.send("ใส่เวลาแบบ HH:MM:SS AM/PM นะครับขอบคุณครับ")
  else:
    await ctx.message.channel.send("Setting alarm for " + fk_time)
    alarm_hour = alarm_time[0:2]
    alarm_min = alarm_time[3:5]
    alarm_sec = alarm_time[6:8]
    alarm_period = alarm_time[8:].upper()

    while True:
      now = datetime.now()

      current_hour = now.strftime("%I")
      current_min = now.strftime("%M")
      current_sec = now.strftime("%S")
      current_period = now.strftime("%p")

      if alarm_period == current_period:
          if alarm_hour == current_hour:
              if alarm_min == current_min:
                  if alarm_sec == current_sec:
                      await ctx.message.channel.send("ไปนอนได้แล้วน้องๆ   เดี๋ยวโดนเขกหัวน้าาาาาาาา")
                      if (ctx.author.voice):
                        channel = ctx.author.voice.channel
                        await channel.connect()
                        playSong(ctx, "https://www.youtube.com/watch?v=hA_0cI1BJhs")
                      break


@client.command(pass_context = True)
async def pause(ctx):
  voice = get (client.voice_clients, guild = ctx.guild)
  
  if voice and voice.is_playing():
    voice.pause()
    await ctx.message.channel.send("music paused")
  else:
    await ctx.message.channel.send("music not playing failed pause")

@client.command(pass_context = True)
async def resume(ctx):
  voice = get (client.voice_clients, guild = ctx.guild)

  if voice and voice.is_paused():
    voice.resume()
    await ctx.send("resumed music")
  else:
    await ctx.send("music is not paused")

@client.command(pass_context = True)
async def skip(ctx):
  voice = get (client.voice_clients, guild = ctx.guild)
  
  if voice and voice.is_playing():
    voice.stop()
    await ctx.message.channel.send("music stopped")
  else:
    await ctx.message.channel.send("music is not playing failed to stop")






def playSong(ctx, url):
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


def is_connected(ctx):
    voice_client = get(client.voice_clients, guild=ctx.guild)
    return 



keep_alive()

client.run('ODQ5OTg3ODM5Mjc3NzkzMjgw.YLjK3A.AA6ZPnjXHXUe4k0x_oiYNqnqq4Y')