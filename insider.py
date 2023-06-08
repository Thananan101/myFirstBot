import discord
from discord.ext import commands
import random
import asyncio
import re

class insider(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.active_timer = None
        
    async def get_ids(self, user_id):
        if type(user_id) == list or type(user_id) == tuple:
            user_ids = [int(re.sub('[<>@!]', '', uid)) for uid in user_id]
        else:
            user_ids = int(re.sub('[<>@!]', '', user_id))
        return user_ids
    
    async def get_member(self, user_id):
      user = await self.client.fetch_user(user_id)
      return user
        
    def get_word(self):
        with open('words.txt', 'r') as file:
            # Read the contents of the file
            content = file.readlines()

        # Remove any trailing newline characters and whitespace
        words = [line.strip() for line in content]
        word = random.choice(words)
        return word

    @commands.Cog.listener()
    async def on_ready(self):
        print('insider is ready!')
    
    @commands.command()
    async def play(self, ctx, *players):
        roles = ['insider', 'host', 'dumb', 'dumb']
        #should have 4 more players
        num_players = len(players) + 1
        if num_players < 4:
            ctx.send('ต้องมีคนเล่นมากกว่า 4 คนครับ')
            return
        elif num_players >= 5:
            num_dumb = num_players - 4
            roles += ['dumb'] * num_dumb
        
        word = self.get_word()
        # Shuffle the second_list randomly
        random.shuffle(roles)

        mapped_list = list(zip(players, roles))
        
        for item in mapped_list:
            player = item[0]
            role = item[1]
            print(player)
            player_id = await self.get_ids(player)
            print(player_id)
            player = await self.get_member(player_id)
            print(player)
            if role == 'host':
                await player.send('คุณได้เป็น HOST นะครับ ดูแลเกมดีๆด้วยล่ะ')
                await player.send(('คำศัพท์ของรอบนี้ก็คือ', word))
            elif role == 'insider':
                await player.send('คุณได้เป็น Insider นะครับ ทำตัวเนียนๆด้วยล่ะ')
                await player.send(('คำศัพท์ของรอบนี้ก็คือ', word))
            elif role == 'dumb':
                await player.send('เป็นชาวบ้านโง่ ๆ สู้ ๆ ละกัน')
            await ctx.send('เกมเริ่ม')    
        async def timer_task():
            await asyncio.sleep(300) # 5 mins
            await ctx.send('จบเกมคับ 5 นาที')
        self.active_timer = asyncio.create_task(timer_task())
    
    @commands.command()
    async def fs(self, ctx):
        if self.active_timer is None:
            await ctx.send("ไม่ได้มีการเล่นเกมอยู่คับ")
        else:
            self.active_timer.cancel()
            self.active_timer = None
            await ctx.send('มีคนใช้อำนาจหยุดเกม')
            
    
def setup(client):
    client.add_cog(insider(client))