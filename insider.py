import discord
from discord.ext import commands
import random
import asyncio
import re
import json

class Insider(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.active_timer = None
        self.players = {}
        self.vote_buttons = {}  # Store the VoteBtn objects here
        self.vote_message = None
    
    async def get_member(self, user_id):
      user = await self.client.fetch_user(user_id)
      return user
  
    async def get_ids(self, user_id):
        if type(user_id) == list or type(user_id) == tuple:
            user_ids = [int(re.sub('[<>@!]', '', str(uid))) for uid in user_id]
        else:
            user_ids = int(re.sub('[<>@!]', '', str(user_id)))
        return user_ids
        
    def get_word(self):
        with open('thai_words.json', 'r', encoding='utf-8') as file:
            content = json.load(file)
        word = random.choice(content)
        return word
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('insider is ready!')
        
    @commands.command()
    async def insider_ping(self, ctx):
        await ctx.send("insider pong!!")
        
    @commands.command()
    async def play(self, ctx, *players):
        players = list(players)  # Convert the tuple to a list
        roles = ['insider', 'host', 'dumb', 'dumb']
        
        
        #check if author tag himself later
        
        #should have 4 more players
        num_players = len(players) + 1
        if num_players < 4:
            await ctx.send('ต้องมีคนเล่นมากกว่า 4 คนครับ')
            return
        elif num_players >= 5:
            num_dumb = num_players - 5
            roles += ['dumb'] * num_dumb
        print(roles)
        word = self.get_word()
        # Shuffle the second_list randomly
        random.shuffle(roles)    
        players = list(zip(players, roles))
        
        for player_item in players:
            player = player_item[0]
            role = player_item[1]

            player_id = await self.get_ids(player)

            player = await self.get_member(player_id)
            item_string = 'คำศัพท์ของรอบนี้ก็คือ {}'.format(word)
            if role == 'host':
                await player.send('คุณได้เป็น HOST นะครับ ดูแลเกมดีๆด้วยล่ะ')
                await player.send(item_string)
            elif role == 'insider':
                await player.send('คุณได้เป็น Insider นะครับ ทำตัวเนียนๆด้วยล่ะ')
                await player.send(item_string)
            elif role == 'dumb':
                await player.send('เป็นชาวบ้านโง่ ๆ สู้ ๆ ละกัน')
            self.players[player.name] = Player(player.name, role)

        async def timer_task():
            await ctx.send('เกมเริ่ม พวกคุณมีเวลา 5 นาที เลทสึโก') 
            await ctx.send('เริ่มจับเวลา')
            await asyncio.sleep(300) # 5 mins
            await ctx.send('จบเกมคับ 5 นาที')
            if self.vote_message is None:
                embed, view = self.start_vote()
                self.vote_message = await ctx.send(embed=embed, view=view)
            else:
                await self.update_vote_count()
        
        self.active_timer = asyncio.create_task(timer_task())
        
    async def start_vote(self):
        embed, view = self.get_embed_vote()
        return embed, view
    
    def get_embed_vote(self):
        view = discord.ui.View()
        for player_name in self.players:
            if self.players[player_name].role == "HOST":
                continue
            vote_count = 0
            try:
                vote_count = self.vote_buttons[player_name].vote_count
            except:
                print('first time voting, no vote count yet')
            vote_button = VoteBtn(player_name, self, vote_count)
            view.add_item(vote_button)
            self.vote_buttons[player_name] = vote_button
        
        
        embed = discord.Embed(
            title="Insider game",
            description="กดปุ่มโหวตคนที่คุณคิดว่าเป็นจอมบงการ (Insider)",
            color=int("1AA7EC", 16)
        )
        embed.set_thumbnail(url="https://github.com/alenros/insider/blob/master/public/ms-icon-144x144.png?raw=true")
        embed.add_field(name="Voting", value="Please cast your vote by clicking the button below.", inline=False)

        for name, button in self.vote_buttons.items():
            embed.add_field(name=name, value=f"Votes: {self.vote_buttons[name].vote_count}", inline=False)
        return embed, view
    
    @commands.command()
    async def vote(self, ctx):
        if not self.vote_message:
            embed, view = await self.start_vote()
            self.vote_message = await ctx.send(embed=embed, view=view)
        else:
            await self.update_vote_count()
            
    async def update_vote_count(self):
        embed, view = self.get_embed_vote()
        await self.vote_message.edit(embed=embed, view=view)
        return embed, view


class Player():
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.vote = None
        
        
class VoteBtn(discord.ui.Button):
    def __init__(self, name, insider_instance, vote_count = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.insider_instance = insider_instance
        self.vote_count = vote_count
        
        # Set the button properties
        self.style = discord.ButtonStyle.primary
        self.label = f"{self.name} (Clicks: {self.vote_count})"
        self.custom_id = f"vote_{str(self.name)}"
        
    async def callback(self, interaction: discord.Interaction):
        print('callback')
        print(self.name)
        user_name = interaction.user.name
        #check for eligible voter
        if self.name not in self.insider_instance.players or self.insider_instance.players[self.name].role == "HOST":
            await interaction.response.send_message("ผู้ดำเนินเกมกับคนที่ไม่เกี่ยวข้องอย่ายุ่งครับ.", ephemeral=True)
        
        #check if already voted
        if self.insider_instance.players[user_name].vote is not None:
            #deduct from previous vote
            prev_vote = self.insider_instance.players[user_name].vote
            prev_button = self.insider_instance.vote_buttons[prev_vote]
            prev_button.vote_count -= 1
            prev_button.label = f"{prev_button.name} (Clicks: {prev_button.vote_count})"
        
        #add score to new vote
        self.vote_count += 1
        self.label = f"{self.name} (Clicks: {self.vote_count})"
        print(self.vote_count)
        self.insider_instance.players[user_name].vote = self.name
        await interaction.response.defer()
        
        #update the vote count
        await self.insider_instance.update_vote_count()
        print('--------')
        
        
            

async def setup(client):
    await client.add_cog(Insider(client)) 