import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand

client = commands.Bot(command_prefix = '$', Intents=discord.Intents.all())

slash = SlashCommand(client, sync_commands=True)


class slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash.slash(name = 'Ping', description ='just testing')
    async def ping(self, ctx: SlashContext):
        embed = discord.Embed(title="embed test")
        await ctx.send(content="test", embeds=[embed])
    
    @client.command(pass_context = True, aliases=["แดง"])
    async def dang(self, ctx):
      await ctx.message.channel.send("ดำ")  
      
def setup(client):
  client.add_cog(slash(client))