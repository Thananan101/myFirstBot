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
from discord_slash import cog_ext, SlashContext, SlashCommand
          
from datetime import datetime   

from os import system

import imaplib
import email

from readEmail import getTcomZoomLink
import levelsys
import music
import slash

import asyncio

import googletrans  
from googletrans import Translator


TOKEN = os.environ['TOKEN']

client = commands.Bot(command_prefix = '$', Intents=discord.Intents.all())


bPuen = ["ไอ่ปืนมันไก่กรู๊กกก", "น้องเกิ๊นน", "กระจอก", "ขี้เมา", "เด็กเหี้ย"]
bLung = ["ไอ้สัสลุง หัดใช้สมองบ้างนะไอ้เหี้ยย", "7 ปีละนะไอ้สัส เมื่อไหร่จะย้ายออกจากข้างบ้านกุซักที"]
bTee = ["ไม่มีคอนโดมาเอากับพี่ <:Tee_smile:850487711420645386>", "ผมไม่ใช่ทีธรรมดา ผมอะทีรัก <:Tee_smile:850487711420645386>"]
bGun = ["ซักหมัดปะมึงอะ ไอ่บูม <:BGummud:841699099249344542>", "มาเดี๋ยวซับน้ำตาให้ แต่ซับด้วยหมัดกูเนี่ยแหละ <:BGummud:841699099249344542>", " อะไรล่ะน้องเอ้ว <:BGummud:841699099249344542>"]
bTen = ["เหล่ท่อ", "ช่วงโควิดต้องใส่แมส ส่วนเตาแก๊สมีไว้จุดไฟ"]



@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Streaming(name="กด Follow hawonx ด้วยนะครับ ^^", url='https://www.twitch.tv/hawonx'))
  levelsys.setup(client)
  music.setup(client)
  slash.setup(client)

@client.event
async def on_message(message):
    # do some extra stuff here
    if message.content == "งอง" or message.content == "ngong":
      await message.channel.send("งอง เชี่ยไรไอ้สัส เดี๋ยวโดนเอิร์ทตบให้ซักป๊าบ")
  
    if message.content.startswith("หยิ่ง"):
      await message.channel.send("จริง ในดิสมีแต่คนหยิ่ง หยิ่งเกิ๊นนนน")

    await client.process_commands(message)

@client.command(pass_context = True)
async def joina(ctx):
  voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice_client == None:
    if (ctx.author.voice):
      channel = ctx.author.voice.channel
      await channel.connect()
      await ctx.send("เข้ามาแล้วขอรับนายท่าน มีอะไรให้รับใช้")
    else:
      await ctx.message.channel.send("เข้าซักห้องก่อนค่อยเรียกกู ไอ่ฟาย")

@client.command(pass_context = True)
async def check(ctx, who):
  print(who[3:-1])


@client.command(pass_context = True)
async def leavea(ctx):
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

@client.command(pass_context = True, aliases=['งอง'])
async def ngong(ctx):
  await ctx.channel.send("งอง เชี่ยไรไอ้สัส เดี๋ยวโดนเอิร์ทตบให้ซักป๊าบ")

# how to use custom emoji: <:emojiName:emojiID> you can get the id from sticker URL
@client.command(pass_context = True, aliases=["ปืน"])
async def puen(ctx):
  await ctx.message.channel.send(bPuen[randrange(len(bPuen))] + " <:kwy:844178327925424138>  <:puenKuan:841398727641137152>")

@client.command(pass_context = True, aliases=["ลุง"])
async def lung(ctx):
  await ctx.message.channel.send(bLung[randrange(len(bLung))] + " :footprints:")

@client.command(pass_context = True, aliases=["เท็น"])
async def ten(ctx):
  await ctx.message.channel.send(bTen[randrange(len(bTen))] +" <:tenenz:841397333136244756>")

@client.command(pass_context = True, aliases=["ชานม", "หนม", "น้ำหวาน", "ขนมนมเนยนุ๊บนิ๊บ"])
async def chanom(ctx):
  await ctx.message.channel.send("ไอ้นั่นมันชื่อภูมิ ไอ้สัส เรียกให้ถูกดิ๊ <:Chandsome:851074765305020476>")

@client.command(pass_context = True, aliases=["ภูมิ"])
async def poom(ctx):
  await ctx.message.channel.send("สวัสดีคร้าบบ ทุกคนนน ผมชื่อภูมินะครับ <:Chandsome:851074765305020476>")

@client.command(pass_context = True, aliases=["ที"])
async def tee(ctx):
  await ctx.message.channel.send(bTee[randrange(len(bTee))])

@client.command(pass_context = True, aliases=["บก", "บิ๊กกัน", "biggun"])
async def bg(ctx):
  await ctx.message.channel.send(bGun[randrange(len(bGun))])


@client.command(pass_context = True, aliases=['PRINCIPLES OF DIGITAL COMMUNICATION AND MODELING', 'digit', 'principle', 'principles', 'comm'])
async def digital(ctx):
  await ctx.message.channel.send("https://us02web.zoom.us/j/84507102474?fbclid=IwAR31Fcy6_iEj9I2Ol6EsTowxlYs1lLjN1PW9di_Vy4_a0b5HKXFn2uruZBU#success รหัส 804401")

@client.command(pass_context = True, aliases=["softN", 'software', 'software engineer', 'swe'])
async def SWE(ctx):
  await ctx.message.channel.send("https://meet.google.com/ioj-xbge-ifb")
	

@client.command(pass_context = True, aliases=["mobile app", 'mobileapp', 'mob-app'])
async def mobile(ctx):
  await ctx.message.channel.send("https://meet.google.com/yns-kzsg-yem?authuser=1")

@client.command(pass_context = True, aliases=["ML","ml"])
async def machine(ctx):
  await ctx.message.channel.send("https://meet.google.com/kfe-zbjn-ufa")


#บอทเข้าห้องไม่ได้ติด channel.connect()

@client.command(pass_context = True)
async def alarm(ctx, alarm_time):
  now = datetime.now()
  fk_time = alarm_time
  validate = validate_time(alarm_time)
  alarm_time = timezoneToTH(alarm_time)
  print(alarm_time)
  print(validate)
  print(len(alarm_time))
  if validate != "ok":
    await ctx.message.channel.send("ใส่เวลาแบบ HH:MM:SSAM/PM นะครับขอบคุณครับ")
  else:
    await ctx.message.channel.send("Setting alarm for " + fk_time)
    alarm_hour = int(alarm_time[0:2])
    alarm_min = int(alarm_time[3:5])
    alarm_sec = int(alarm_time[6:8])
    alarm_period = alarm_time[8:].upper()
    seconds_hms = [3600, 60, 1] 
    print(alarm_hour)
    print(alarm_min)
    print(alarm_sec)
    print(alarm_period)
    current_hour = int(now.strftime("%I"))
    current_min = int(now.strftime("%M"))
    current_sec = int(now.strftime("%S"))
    current_period = now.strftime("%p")
    diffH = alarm_hour - current_hour
    diffM = alarm_min - current_min
    diffS = alarm_sec - current_sec
    diffP = int(alarm_period != current_period)
    diffT = diffS + diffM*60 + diffH*60*60 + diffP*60*60*12
    print(diffT)

    await asyncio.sleep(diffT)
    await ctx.message.channel.send("ไปนอนได้แล้วน้องๆ   เดี๋ยวโดนเขกหัวน้าาาาาาาา")
    if (ctx.author.voice):
      channel = ctx.author.voice.channel
      await channel.connect()
      playSong(ctx, "https://www.youtube.com/watch?v=hA_0cI1BJhs")      


@client.command(pass_context = True, aliases=["t", "เวลา"])
async def time(ctx):
  now = datetime.now()
  current_hour = int(now.strftime("%-H")) + 7
  current_min = now.strftime("%M")
  current_sec = now.strftime("%S")
  current_period = "AM" if now.strftime("%p")=="PM" else "PM"

  if current_hour >= 24:
    current_hour -= 24
    if current_hour < 10:
      current_hour = "0" + str(current_hour)
  print("ขณะนี้เวลา: {}:{}:{} {}".format(current_hour, current_min, current_sec, current_period))
  await ctx.message.channel.send("ขณะนี้เวลา: {}:{}:{} {}".format(current_hour, current_min, current_sec, current_period))


#unuseable
@client.command(pass_context = True, aliases=['tr', 'แปล'])
async def translate(ctx, *, args):
  text = ' '.join(args)
  translator = Translator()
  lang = translator.detect(text).lang
  txt_translated = translator.translate(args, src=lang, dest='th')
  await ctx.send(txt_translated)




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

@client.command(pass_context = True, aliases=["Tcom", "Theory"])
async def theory(ctx):
  links = getTcomZoomLink()
  for i, link in enumerate(links):
    if i == 0:
      await ctx.channel.send('here is the 1st link: {}'.format(link))
    elif i == 1:
      await ctx.channel.send('here is the 2nd link: {}'.format(link))


keep_alive()

client.run(TOKEN)