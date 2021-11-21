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
          self.newplayer(message.author)
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

    @commands.command(aliases=['rank', 'Rank', 'ranking'])
    async def rankings(self, ctx):
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

    @commands.command()
    async def leaderboard(self, ctx):
      rankings = playerDB.find().sort('Kill', -1)
      i = 1
      embed = discord.Embed(title='Rankings:')
      for x in rankings:
        print(x)
        try:
          temp = await ctx.guild.fetch_member(x['id'])
          tempKill = x['Kill']
          tempDeath = x['death']
          embed.add_field(name=f"{i}: {temp.name}",value=f"K/D: {tempKill}/{tempDeath}", inline=False)
          i += 1
        except:
          pass
        if i == 11:
          break
      await ctx.channel.send(embed=embed)

    @commands.command(aliases=["profile", "pro", "stat"])
    async def status(self, ctx):
      player = playerDB.find_one({"id": ctx.author.id})
      await self.hpRegen(player)
      await self.reviveDeeMai(player)
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
        embed = discord.Embed(title="{}'s stats".format(ctx.author.name))
        embed.add_field(name="Name", value=ctx.author.mention, inline = True)
        embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline = True)
        embed.add_field(name="level", value=f"{lvl}", inline = True)
        embed.add_field(name="HP", value=f"{HP}/{HPmax}", inline = True)
        embed.add_field(name="Alive?", value=f"{player['alive']}", inline = True)
        embed.add_field(name="HP bar", value=boxes * ":red_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
      
    @commands.command(aliases=["ต่อย", "กำหมัดไปซัดหน้า"])
    async def punch(self, ctx, punch: discord.Member):
      attacker = ctx.author.name
      attacked = punch.name
      puncher = playerDB.find_one({"id": ctx.author.id})
      punched = playerDB.find_one({"id": punch.id})
      if puncher is None:
          self.newplayer(punch)
          punched = playerDB.find_one({"id": punch.id})
      if punched is None:
          self.newplayer(punch)
          punched = playerDB.find_one({"id": punch.id})
      await self.hpRegen(puncher)
      await self.hpRegen(punched)
      await self.reviveDeeMai(punched)
      await self.reviveDeeMai(puncher)
      puncher = playerDB.find_one({"id": ctx.author.id})
      punched = playerDB.find_one({"id": punch.id})

      if not self.isAlive(puncher):
        await ctx.channel.send("คุณมึงตายอยู่ครับ คนตายก็อยู่นิ่งๆดิ๊")
        return
      if not self.isAlive(punched):
        await ctx.channel.send("คุณ {} เขาตายอยู่นะครับ รบกวนอย่าซ้ำศพนะครับเพื่อสังคมที่ดี ^^".format(attacked))
        return
      if self.isCD(puncher['prevSkillTime'], puncher['CD']):
        print(f'{attacker} ต่อย {attacked} {punch.id}')
        crit = randrange(100) < 10 #boolean 10% critical rate
        dmg = randrange(120)
        if crit:
          dmg = dmg*1.5
          await ctx.channel.send("ต่อยแบบติดคริติค่อน!!")
        if punched['HP'] > dmg:
          hp = punched['HP'] - dmg
          playerDB.update_one({'id':punched['id']}, {'$set':{'HP':hp}})
          await ctx.channel.send("{} ต่อย {} ด้วยความแรง {} damge".format(attacker, attacked, dmg))
          await ctx.channel.send("{}'s HP: {}".format(attacked, hp)) 
        else:
          playerDB.update_one({'id':punched['id']}, {'$set':{'HP':0}})
          playerDB.update_one({'id':punched['id']}, {'$set':{'alive':False}})
          playerDB.update_one({'id':punched['id']}, {'$set':{'died':datetime.datetime.now().replace(microsecond=0)}})
          await ctx.channel.send("{} ต่อยเข้าไปที่หน้าของ {} ด้วยความแรง {} damge".format(attacker, attacked, dmg))
          await ctx.channel.send("{}'s dea``d. RIP กากเกิ๊นนน".format(attacked)) 
          xp = puncher['xp'] + 50
          kills = puncher['kill'] + 1
          dead = punched['death'] + 1
          playerDB.update_one({'id':puncher['id']}, {'$set':{'xp':xp}})    
          playerDB.update_one({'id':puncher['id']}, {'$set':{'kill': kills}})
          playerDB.update_one({'id':punched['id']}, {'$set':{'death':dead}})   

        playerDB.update_one({'id':puncher['id']}, {'$set':{'CD':30}})
        playerDB.update_one({'id':puncher['id']}, {'$set':{'prevSkillTime':datetime.datetime.now()}})
      else:
        await ctx.channel.send('ใจเย็นๆนะ ยังต่อยไม่ได้ รู้อยากว้อนแต่กำหมัดไว้ก่อน')
    
    def isCD(self, prev, cd):
      now = datetime.datetime.now()
      diff = now - prev
      return True if int(diff.seconds) > cd else False
    
    def isAlive(self, player):
      if not player['alive']:
        return False
      else:
        return True

    async def reviveDeeMai(self, player):
      if not player['alive']:
        #if player is dead
        print(player['alive'])
        now = datetime.datetime.now().replace(microsecond=0)
        died = player['died']
        diff = now-died
        if diff.seconds >= 600:
          hpmax = player['HPmax']
          playerDB.update_one({'id': player['id']}, {'$set':{'alive':True}})
          playerDB.update_one({'id': player['id']}, {'$set':{'HP':hpmax}})
          playerDB.update_one({'id': player['id']}, {'$set':{'lastRegen':datetime.datetime.now().replace(microsecond=0)}})


    def newplayer(self, player):
      newuser = {"id" : player.id, "xp" : 0, "HPmax": 200, "alive":True, "level":1, "HP": 200, "CD":0, "prevSkillTime":datetime.datetime.now().replace(microsecond=0), 
      "lastRegen":datetime.datetime.now().replace(microsecond=0), 
      "died":0}
      playerDB.insert_one(newuser)

    async def hpRegen(self, player):
      '''
      For the time being, I'm using hpregen = 10/minutes, which means that if the difference is greater than 1 minute, we heal the player.

      bug: sometimes it doesn't heal i don't know why...
      '''
      prev = player['lastRegen']
      now = datetime.datetime.now().replace(microsecond=0)
      diff = now-prev 
      if int(diff.seconds/60) < 1:
        return
      else:
        heal = int(diff.seconds/60) * 2
        if player['HP'] + heal > player['HPmax']:
          current_hp = player['HPmax']
        else:
          current_hp = player['HP'] + heal
        playerDB.update_one({'id':player['id']}, {'$set':{'HP':current_hp}})
        playerDB.update_one({'id':player['id']}, {'$set':{'lastRegen': datetime.datetime.now().replace(microsecond=0)}})
        

    @commands.command(aliases=["สั่งฆ่า"])
    async def kill(self, ctx, punch: discord.Member):
      attacker = ctx.author.name
      attacked = punch.name
      puncher = playerDB.find_one({"id": ctx.author.id})
      punched = playerDB.find_one({"id": punch.id})
      if ctx.author.id == 313326050090156032:
          await ctx.channel.send("{} สั่งฆ่า {} ด้วยความแรง 999999999 damge".format(attacker, attacked))
          await ctx.channel.send("{}'s dead. RIP กากเกิ๊นนน".format(attacked))
          playerDB.update_one({'id':punched['id']}, {'$set':{'HP':0}})
          playerDB.update_one({'id':punched['id']}, {'$set':{'alive':False}})
          playerDB.update_one({'id':punched['id']}, {'$set':{'died':datetime.datetime.now().replace(microsecond=0)}})
      else:
        await ctx.channel.send("ไม่ใช่ GM ใช้ไม่ได้ครับน้อง ๆ")

    @commands.command(aliases=['ฮีล'])
    async def heal(self, ctx, who: discord.Member):
      if who is None:
        who = ctx.author
      player = playerDB.find_one({'id':who.id})
      healer = playerDB.find_one({'id':ctx.author.id})
      heal = randrange(40, 70)
      await self.hpRegen(player)
      await self.reviveDeeMai(player)
      if self.isCD(healer['prevSkillTime'], healer['CD']):
        if player['HP'] + heal > player['HPmax']:
            current_hp = player['HPmax']
        else:
            current_hp = player['HP'] + heal
        await ctx.channel.send('{} heals {} for {} HP'.format(ctx.author.name, who.name, heal))
        playerDB.update_one({'id':player['id']}, {'$set':{'HP':current_hp}})
        playerDB.update_one({'id':healer['id']}, {'$set':{'CD':60}})
        playerDB.update_one({'id':healer['id']}, {'$set':{'prevSkillTime':datetime.datetime.now()}})
      else:
        await ctx.channel.send("ติด CD ครับ")
    


    @commands.command()
    async def resetHP(self, ctx):
      if ctx.author.id == 313326050090156032:
        playerDB.update_many({}, {"$set": {"HP":200}})
        playerDB.update_many({}, {"$set": {"alive":True}})
        playerDB.update_many({}, {'$set':{'lastRegen':datetime.datetime.now().replace(microsecond=0)}})
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
    
    @commands.command()
    async def updateDB(self, ctx):
      """
      this is use to update anything (new i guess) to MongoDB 
      just because i tried console and it doesn't work so i build this 
      function for me.
      """
      if ctx.author.id == 313326050090156032:
        playerDB.update_many({}, {'$set': {'Kill':0}})
        playerDB.update_many({}, {'$set': {'death':0}})

def setup(client):
  client.add_cog(levelsys(client))