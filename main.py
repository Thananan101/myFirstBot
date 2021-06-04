import discord
import os 
from random import randrange
from replit import db
from keep_awake import keep_alive
from discord.ext import commands

client = commands.Bot(command_prefix = '$')

bPuen = ["ไอ่ปืนมันไก่กรู๊กกก", "น้องเกิ๊นน", "กระจอก", "ขี้เมา"]

bLung = ["ไอ้สัสลุง หัดใช้สมองบ้างนะไอ้เหี้ยย", "7 ปีละนะไอ้สัส เมื่อไหร่จะย้ายออกจากข้างบ้านกุซักที"]

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))
  

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
  


@client.command(pass_context = True)
async def join(ctx):
  channel = ctx.message.author.voice.voice_channel
  await client.join_voice_channel(channel)
  
keep_alive()

client.run('ODQ5OTg3ODM5Mjc3NzkzMjgw.YLjK3A.AA6ZPnjXHXUe4k0x_oiYNqnqq4Y')