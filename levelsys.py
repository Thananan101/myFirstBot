#https://www.youtube.com/watch?v=qaJ58rrv_PM&t=323s
import discord 
from discord.ext import commands
from pymongo import MongoClient
from random import randrange
import asyncio
import time

cluster = MongoClient("mongodb+srv://feelsgoodnow:Q2ES0RzLqhpR6pzU@depresseddiscordbot.1fkbd.mongodb.net/test?retryWrites=true&w=majority")

levelling = cluster["depressedBot"]["levelling"]

class levelsys(commands.Cog):
    def __init__(self, client):
      self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print("levelsys is ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
      stats = levelling.find_one({"id" : message.author.id})
      if not message.author.bot:
        if stats is None:
          newuser = {"id" : message.author.id, "xp" : 0, "HPcap": 200, "Alive":True, "level":1, "HP": 200, "CD":0, "prevSkillTime":0}
          levelling.insert_one(newuser)
        else:
          xp = stats["xp"] + 5
          levelling.update_one({"id":message.author.id}, {"$set":{"xp":xp}})
          lvl = 0
          while True:
            if xp < ((50*(lvl**2)) + (50*lvl)):
              break
            lvl += 1
          xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
          if xp == 0:
            await message.channel.send(f"well done {message.author.mention}! You leveled up to **level: {lvl}**")
            HPcap = stats["HPcap"]+20
            levelling.update_one({"id":message.author.id}, {"$set":{"level":lvl}})
            levelling.update_one({"id":message.author.id}, {"$set":{"HP":HPcap}})
            levelling.update_one({"id":message.author.id}, {"$set":{"HPcap":HPcap}})

    @commands.command()
    async def rank(self,ctx):
      stats = levelling.find_one({"id": ctx.author.id})
      if stats is None:
        embed = discord.Embed(description="You haven't sent any messages, no rank for you!!")
        await ctx.message.channel.send(embed=embed)
      else:
        xp = stats["xp"]
        lvl = stats["level"]
        rank = 0
        xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
        boxes = int((lvl/(200*((1/2) * lvl)))*20)
        rankings = levelling.find().sort("xp",-1)
        for x in rankings:
          rank += 1
          if stats["id"] == x["id"]:
            break
        embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
        embed.add_field(name="Name", value=ctx.author.mention, inline = True)
        embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline = True)
        embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline = True)
        embed.add_field(name="level", value=f"{lvl}", inline = True)
        embed.add_field(name="Progress Bar (lvl)", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
      rankings = levelling.find().sort("xp", -1)
      i = 1
      embed = discord.Embed(title="Rankings:")
      for x in rankings:
        print(x)
        try:
          temp = await ctx.guild.fetch_member(x["id"])
          tempxp = x["xp"]
          embed.add_field(name=f"{i}: {temp.name}",value=f"Total XP: {tempxp}", inline=False)
          i += 1
        except:
          pass
        if i == 11:
          break
      await ctx.channel.send(embed=embed)

    @commands.command(aliases=["profile", "pro", "stat"])
    async def status(self, ctx):
      player = levelling.find_one({"id": ctx.author.id})
      if player is None:
        embed = discord.Embed(description="You haven't sent any messages, no rank for you!!")
        await ctx.message.channel.send(embed=embed)
      else:
        xp = player['xp']
        lvl = player['level']
        HP = player['HP']
        xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
        HPcap = player['HPcap']
        boxes = int((HP/HPcap)*20)
        embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
        embed.add_field(name="Name", value=ctx.author.mention, inline = True)
        embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline = True)
        embed.add_field(name="level", value=f"{lvl}", inline = True)
        embed.add_field(name="HP", value=f"{HP}/{HPcap}", inline = True)
        embed.add_field(name="HP bar", value=boxes * ":red_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
      
    @commands.command()
    async def punch(self, ctx, punch: discord.Member):
      attacker = ctx.author.name
      attacked = punch.name
      puncher = levelling.find_one({"id": ctx.author.id})
      punched = levelling.find_one({"id": punch.id})
      if True:
        dmg = randrange(100)
        hp = punched['HP'] - dmg
        if hp > 0:
          await ctx.channel.send("{} punch {} for {} damge".format(attacker, attacked, dmg))
          await ctx.channel.send("{}'s HP: {}".format(attacked, hp))
          levelling.update_one({"id":punched['id']}, {"$set":{"HP":hp}})
          levelling.update_one({"id":puncher['id']}, {"$set":{"CD":True}})
          await asyncio.sleep(600)
          levelling.update_one({"id":puncher['id']}, {"$set":{"CD":False}})
        else:
          await ctx.channel.send("{} punch {} for {} damge".format(attacker, attacked, dmg))
          await ctx.channel.send("{}'s dead. RIP กากเกิ๊นนน".format(attacked))
          levelling.update_one({"id":punched['id']}, {"$set":{"HP":0}})
          levelling.update_one({"id":punched['id']}, {"$set":{"Alive":False}})
          levelling.update_one({"id":puncher['id']}, {"$set":{"CD":True}})
          await asyncio.sleep(300)
          levelling.update_one({"id":punched['id']}, {"$set":{"Alive":True}})
          await asyncio.sleep(300)
          levelling.update_one({"id":puncher['id']}, {"$set":{"CD":False}})
      else:
        await ctx.channel.send("ใจเย็น ๆ ดิ๊มึงติดคูลดาวน์อยู่ กำหมัดรอไว้เลยเดี๋ยวได้ต่อยแน่")
        
    @commands.command(aliases=["สั่งฆ่า"])
    async def kill(self, ctx, punch: discord.Member):
      attacker = ctx.author.name
      attacked = punch.name
      puncher = levelling.find_one({"id": ctx.author.id})
      punched = levelling.find_one({"id": punch.id})
      if ctx.author.id == 313326050090156032:
          await ctx.channel.send("{} สั่งฆ่า {} ด้วยความแรง 999999999 damge".format(attacker, attacked))
          await ctx.channel.send("{}'s dead. RIP กากเกิ๊นนน".format(attacked))
          levelling.update_one({"id":punched['id']}, {"$set":{"HP":0}})
          levelling.update_one({"id":punched['id']}, {"$set":{"Alive":False}})
          levelling.update_one({"id":puncher['id']}, {"$set":{"CD":True}})
          await asyncio.sleep(300)
          levelling.update_one({"id":punched['id']}, {"$set":{"Alive":True}})
          await asyncio.sleep(300)
          levelling.update_one({"id":puncher['id']}, {"$set":{"CD":False}})
      else:
        await ctx.channel.send("ไม่ใช่ GM ใช้ไม่ได้ครับน้อง ๆ")

    @commands.command()
    async def resetHP(self, ctx):
      if ctx.author.id == 313326050090156032:
        levelling.update_one({}, {"$set": {"HP":200}})
      else:
        await ctx.channel.send("คำสั่งสำหรับ GM ไว้รีเซตเลือดเฉยๆครับ")
def setup(client):
  client.add_cog(levelsys(client))