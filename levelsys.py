#https://www.youtube.com/watch?v=qaJ58rrv_PM&t=323s
import discord 
from discord.ext import commands
from pymongo import MongoClient
from random import randrange
import asyncio
import time
import datetime

cluster = MongoClient("mongodb+srv://feelsgoodnow:Q2ES0RzLqhpR6pzU@depresseddiscordbot.1fkbd.mongodb.net/test?retryWrites=true&w=majority")

playerDB = cluster["depressedBot"]["playerDB"]

class levelsys(commands.Cog):
    def __init__(self, client):
      self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
      print("levelsys is ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
      stats = playerDB.find_one({"id" : message.author.id})
      if not message.author.bot:
        if stats is None:
          newuser = {"id" : message.author.id, "xp" : 0, "HPmax": 200, "Alive":True, "level":1, "HP": 200, "CD":0, "prevSkillTime":0}
          playerDB.insert_one(newuser)
          stats = playerDB.find_one({"id" : message.author.id})
        else:
          xp = stats["xp"] + 5
          playerDB.update_one({"id":message.author.id}, {"$set":{"xp":xp}})
          lvl = 0
          while True:
            if xp < ((50*(lvl**2)) + (50*lvl)):
              break
            lvl += 1
          xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
          if xp == 0:
            await message.channel.send(f"well done {message.author.mention}! You leveled up to **level: {lvl}**")
            HPmax = stats["HPmax"]+20
            playerDB.update_one({"id":message.author.id}, {"$set":{"level":lvl}})
            playerDB.update_one({"id":message.author.id}, {"$set":{"HP":HPmax}})
            playerDB.update_one({"id":message.author.id}, {"$set":{"HPmax":HPmax}})

    @commands.command()
    async def rank(self,ctx):
      stats = playerDB.find_one({"id": ctx.author.id})
      if stats is None:
        embed = discord.Embed(description="You haven't sent any messages, no rank for you!!")
        await ctx.message.channel.send(embed=embed)
      else:
        xp = stats["xp"]
        lvl = stats["level"]
        rank = 0
        xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
        boxes = int((xp/(200*((1/2) * lvl)))*20)
        rankings = playerDB.find().sort("xp",-1)
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
      rankings = playerDB.find().sort("xp", -1)
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
      player = playerDB.find_one({"id": ctx.author.id})
      if player is None:
        embed = discord.Embed(description="You haven't sent any messages, no rank for you!!")
        await ctx.message.channel.send(embed=embed)
      else:
        xp = player['xp']
        lvl = player['level']
        HP = player['HP']
        xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
        HPmax = player['HPmax']
        boxes = int((HP/HPmax)*20)
        embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
        embed.add_field(name="Name", value=ctx.author.mention, inline = True)
        embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline = True)
        embed.add_field(name="level", value=f"{lvl}", inline = True)
        embed.add_field(name="HP", value=f"{HP}/{HPmax}", inline = True)
        embed.add_field(name="HP bar", value=boxes * ":red_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
      
    @commands.command(aliases=["ต่อย", "กำหมัดไปซัดหน้า"])
    async def punch(self, ctx, punch: discord.Member):
      attacker = ctx.author.name
      attacked = punch.name
      puncher = playerDB.find_one({"id": ctx.author.id})
      punched = playerDB.find_one({"id": punch.id})
      if punched is None:
          newuser = {"id" : punch.id, "xp" : 0, "HPmax": 200, "level":1, "HP": 200, "CD":0, "prevSkillTime":datetime.datetime.now().replace(microsecond=0)}
          playerDB.insert_one(newuser)
      
      if self.isCD(puncher['prevSkillTime'], puncher['CD']):
        dmg = randrange(100)
        if punched['HP'] > dmg:
          hp = punched['HP'] - dmg
          playerDB.update_one({'id':puncher['id']}, {'$set':{'HP':hp}})
          await ctx.channel.send("{} ต่อย {} ด้วยความแรง {} damge".format(attacker, attacked, dmg))
          await ctx.channel.send("{}'s HP: {}".format(attacked, hp)) 
        else:
          playerDB.update_one({'id':puncher['id']}, {'$set':{'HP':0}})
          await ctx.channel.send("{} สั่งฆ่า {} ด้วยความแรง 999999999 damge".format(attacker, attacked))
          await ctx.channel.send("{}'s dead. RIP กากเกิ๊นนน".format(attacked))        

        playerDB.update_one({'id':puncher['id']}, {'$set':{'CD':60}})
        playerDB.update_one({'id':puncher['id']}, {'$set':{'prevSkillTime':datetime.datetime.now()}})
      else:
        await ctx.channel.send('ต่อยไม่ได้')
    
    def isCD(self, prev, cd):
      now = datetime.datetime.now()
      diff = now - prev
      return True if int(diff.seconds) > cd else False
      
        
    @commands.command(aliases=["สั่งฆ่า"])
    async def kill(self, ctx, punch: discord.Member):
      attacker = ctx.author.name
      attacked = punch.name
      puncher = playerDB.find_one({"id": ctx.author.id})
      punched = playerDB.find_one({"id": punch.id})
      if ctx.author.id == 313326050090156032:
          await ctx.channel.send("{} สั่งฆ่า {} ด้วยความแรง 999999999 damge".format(attacker, attacked))
          await ctx.channel.send("{}'s dead. RIP กากเกิ๊นนน".format(attacked))
          playerDB.update_one({"id":punched['id']}, {"$set":{"HP":0}})
          playerDB.update_one({"id":punched['id']}, {"$set":{"Alive":False}})
          playerDB.update_one({"id":puncher['id']}, {"$set":{"CD":True}})
          await asyncio.sleep(300)
          playerDB.update_one({"id":punched['id']}, {"$set":{"Alive":True}})
          await asyncio.sleep(300)
          playerDB.update_one({"id":puncher['id']}, {"$set":{"CD":False}})
      else:
        await ctx.channel.send("ไม่ใช่ GM ใช้ไม่ได้ครับน้อง ๆ")

    @commands.command()
    async def resetHP(self, ctx):
      if ctx.author.id == 313326050090156032:
        playerDB.update_many({}, {"$set": {"HP":200}})
      else:
        await ctx.channel.send("คำสั่งสำหรับ GM ไว้รีเซตเลือดเฉยๆครับ")
    
    @commands.command()
    async def c(self, ctx):
      a = datetime.datetime.now().replace(microsecond=0)
      await asyncio.sleep(61)
      b = datetime.datetime.now().replace(microsecond=0)

      print(a)
      print(type(a))
      print(b)
      timediff = b-a
      print(timediff.seconds)
      

def setup(client):
  client.add_cog(levelsys(client))