import discord
import os 
from random import randrange
from replit import db
from keep_awake import keep_alive
from discord.ext import commands

TOKEN = ('ODQ5OTg3ODM5Mjc3NzkzMjgw.YLjK3A.AA6ZPnjXHXUe4k0x_oiYNqnqq4Y')

client = commands.Bot(command_prefix = '$')

bPuen = ["ไอ่ปืนมันไก่กรู๊กกก", "น้องเกิ๊นน", "กระจอก", "ขี้เมา", "เด็กเหี้ย"]
bLung = ["ไอ้สัสลุง หัดใช้สมองบ้างนะไอ้เหี้ยย", "7 ปีละนะไอ้สัส เมื่อไหร่จะย้ายออกจากข้างบ้านกุซักที"]


@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))
  

@client.command(pass_context = True)
async def join(ctx):
  if (ctx.author.voice):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send("เข้ามาแล้วขอรับนายท่าน มีอะไรให้รับใช้")
  else:
    await ctx.message.channel.send("เข้าซักห้องก่อนค่อยเรียกกู ไอ่ฟาย")
  

@client.command(pass_context = True)
async def leave(ctx):
  if (ctx.voice_client):
    await ctx.voice_client.disconnect()
    await ctx.send("ไปละ บัยยย")
  else:
    await ctx.send("ไม่ กูไม่ออก ออกแล้วจะเอาอะไรแดก")

@client.command(pass_context = True)
async def ping(ctx):
  await ctx.message.channel.send("Pong")

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$hello'):
    await message.channel.send('hello there.')
  
  if message.content.startswith('$roll'):
    await message.channel.send(message.author.mention + "  " + str(randrange(100)))

  if message.content.startswith('$หยิ่ง'):
    await message.channel.send("จริง ในดิสมีแต่คนหยิ่ง หยิ่งเกิ๊นนนน")

  if message.content.startswith('$เอ้ว'):
    await message.channel.send("Jett korean อะ seoldam แต่น้องเอ้วอะ so hot")
  
  if message.content.startswith('$ปืน'):
    await message.channel.send(bPuen[randrange(len(bPuen))] + " :footprints:")

  if message.content.startswith('$เท็น'):
    await message.channel.send("เหล่ท่อ")
  
  if message.content.startswith('$ลุง'):
    await message.channel.send(bLung[randrange(len(bLung))] + " :footprints:")



keep_alive()

client.run(TOKEN)