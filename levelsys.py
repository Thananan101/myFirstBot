#https://www.youtube.com/watch?v=qaJ58rrv_PM&t=323s
import discord 
from discord.ext import commands
from pymongo import MongoClient

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
          newuser = {"id" : message.author.id, "xp" : 0}
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
    @commands.command()
    async def rank(self,ctx):
      stats = levelling.find_one({"id": ctx.author.id})
      if stats is None:
        embed = discord.Embed(description="You haven't sent any messages, no rank for you!!")
        await ctx.message.channel.send(embed=embed)
      else:
        xp = stats["xp"]
        lvl = 0
        rank = 0
        while True:
          if xp < ((50*(lvl**2)) + (50*lvl)):
            break
          lvl += 1
        xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
        boxes = int((xp/(200*((1/2) * lvl)))*20)
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

def setup(client):
  client.add_cog(levelsys(client))