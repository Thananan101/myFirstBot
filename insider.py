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
        self.host_disabled = True
    
    async def get_member(self, user_id):
      user = await self.client.fetch_user(user_id)
      return user
  
    async def get_ids(self, user_id):
        if isinstance(user_id, (list, tuple)):
            user_ids = [int(re.sub('[<>@!]', '', str(uid))) for uid in user_id]
        else:
            user_ids = int(re.sub('[<>@!]', '', str(user_id)))
        return user_ids
        
    def get_word(self):
        with open('thai_words.json', 'r', encoding='utf-8') as file:
            content = json.load(file)
        word = random.choice(content)
        return word
    
    async def check_vote(self):
        vote_counts = [button.vote_count for button in self.vote_buttons.values()]
        max_vote_count = max(vote_counts)
        
    
        if vote_counts.count(max_vote_count) == 1:
            max_vote_player = next(
            (player for player, button in self.vote_buttons.items() if button.vote_count == max_vote_count), None
            )
            if max_vote_player:
                await self.vote_message.channel.send("เกมจบลงแล้วครับ!")
                await self.vote_message.channel.send("ผู้ที่ถูกโหวตมากสุดก็คือ {}".format(max_vote_player))
                # delete the timer task
                if self.active_timer is not None:
                    self.active_timer.cancel()
                # ask if they want to play again
                #create a button to ask if they want to play again
                #if yes, call play again
                play_again_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="เล่นอีกครั้ง")
            
                async def play_again_callback(interaction: discord.Interaction):
                    clicked = False
                    #ยังไม่เคย test condition นี้เลย mark หัวไว้
                    if interaction.user.name not in self.players:
                        await interaction.response.send_message("ผู้ดำเนินเกมกับคนที่ไม่เกี่ยวข้องอย่ายุ่งครับ.", ephemeral=True)
                    else:
                        if not clicked:
                            clicked = True
                            await interaction.response.defer()
                            # Delete the play_again_button
                            await interaction.message.delete()
                            
                            # Delete the original vote message
                            await self.vote_message.delete()
                            
                            await self.vote_message.channel.send("{} กดปุ่มเพื่อเริ่มเกมใหม่".format(interaction.user.mention))
            
                            # Call the play command again
                            await self.play(interaction.channel, *[player.id for player in self.players.values()])
                    
                play_again_button.callback = play_again_callback
                view = discord.ui.View()
                view.add_item(play_again_button)
                await self.vote_message.channel.send("คุณต้องการเล่นอีกครั้งหรือไม่?", view=view)
                self.vote_message = None
                self.vote_buttons = {}
                self.host_disabled = True
                
        else:
            self.host_disabled = False
            await self.vote_message.channel.send("มีคนโหวตเท่ากัน ไอ่ Master ออกมาใช้สิทธิ์ใช้เสียงได้ละ")
            
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('insider is ready!')
        
    @commands.command()
    async def insider_ping(self, ctx):
        await ctx.send("insider pong!!")
        
    @commands.command()
    async def play(self, ctx, *players):
        players = list(players)  # Convert the tuple to a list
        roles = ['INSIDER', 'MASTER', 'dumb', 'dumb']
        
        
        #check if author tag himself later
        
        #should have 4 more players
        num_players = len(players) + 1
        if num_players < 4:
            await ctx.send('ต้องมีคนเล่นมากกว่า 4 คนครับ')
            return
        elif num_players >= 5:
            num_dumb = num_players - 5
            roles += ['dumb'] * num_dumb
        elif num_players > 10:
            await ctx.send('ต้องมีคนเล่นไม่เกิน 10 คนครับ')
            return
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
            if role == 'MASTER':
                await player.send('คุณได้เป็น MASTER นะครับ ดูแลเกมดีๆด้วยล่ะ')
                await player.send(item_string)
            elif role == 'INSIDER':
                await player.send('คุณได้เป็น INSIDER นะครับ ทำตัวเนียนๆด้วยล่ะ')
                await player.send(item_string)
            elif role == 'dumb':
                await player.send('เป็นชาวบ้านโง่ ๆ สู้ ๆ ละกัน')
            await player.send('-------------------------')
            self.players[player.name] = Player(player.name, role, player_id)

        async def timer_task():
            await ctx.send('เกมเริ่ม พวกคุณมีเวลา 5 นาที เลทสึโก') 
            await ctx.send('เริ่มจับเวลา')
            await asyncio.sleep(300) # 5 mins
            await ctx.send('จบเกมคับ 5 นาที')
            await ctx.send('หาคำศัพท์ไม่ได้ภายในเวลาที่กำหนด ถือว่าไม่มีใครชนะ')
        
        self.active_timer = asyncio.create_task(timer_task())
        
    async def start_vote(self):
        embed, view = self.get_embed_vote()
        return embed, view
    
    def get_embed_vote(self):
        view = discord.ui.View()
        for player_name in self.players:
            if self.players[player_name].role == "MASTER":
                continue
            vote_count = 0
            vote_button = self.vote_buttons.get(player_name)
            if vote_button is not None:
                vote_count = vote_button.vote_count
            vote_button = VoteBtn(player_name, self, vote_count)
            view.add_item(vote_button)
            self.vote_buttons[player_name] = vote_button
        
        
        embed = discord.Embed(
            title="Insider game",
            description="กดปุ่มโหวตคนที่คุณคิดว่าเป็นจอมบงการ (insider)",
            color=int("1AA7EC", 16)
        )
        embed.set_thumbnail(url="https://github.com/alenros/insider/blob/master/public/favicon-96x96.png?raw=true")
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
    
    @commands.command()
    async def new_vote(self, ctx):
        self.vote_message = None
        self.vote_buttons = {}
        self.host_disabled = True
        await ctx.send("เริ่มโหวตใหม่แล้วครับ")
        embed, view = self.get_embed_vote()
        return embed, view
            
    async def update_vote_count(self):
        embed, view = self.get_embed_vote()
        await self.vote_message.edit(embed=embed, view=view)
        #check if total of voted in the vote buttons is equal to the number of players
        total_votes = 0
        for button in self.vote_buttons.values():
            total_votes += button.vote_count
        if total_votes >= len(self.players) - 1:
            await self.check_vote()
            
        return embed, view
    


class Player():
    def __init__(self, name, role, id):
        self.name = name
        self.role = role
        self.id = id
        self.vote = None
        
        
        
class VoteBtn(discord.ui.Button):
    def __init__(self, name, insider_instance, vote_count = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.insider_instance = insider_instance
        self.vote_count = vote_count
        
        # Set the button properties
        self.style = discord.ButtonStyle.primary
        self.label = f"{self.name}"
        self.custom_id = f"vote_{str(self.name)}"
        
    async def callback(self, interaction: discord.Interaction):
        print('callback')
        print(self.name)
        user_name = interaction.user.name
        #check for eligible voter
        if self.name not in self.insider_instance.players or (self.insider_instance.players[user_name].role == "MASTER" and self.insider_instance.host_disabled):
            await interaction.response.send_message("ผู้ดำเนินเกมกับคนที่ไม่เกี่ยวข้องอย่ายุ่งครับ.", ephemeral=True)
        
        #check if already voted
        if self.insider_instance.players[user_name].vote is not None:
            #deduct from previous vote
            prev_vote = self.insider_instance.players[user_name].vote
            prev_button = self.insider_instance.vote_buttons[prev_vote]
            prev_button.vote_count -= 1
            prev_button.label = f"{prev_button.name}"
        
        #add score to new vote
        self.vote_count += 1
        self.label = f"{self.name}"
        print(self.vote_count)
        self.insider_instance.players[user_name].vote = self.name
        await interaction.response.defer()
        
        #update the vote count
        await self.insider_instance.update_vote_count()
        print('--------')
        
        
            

async def setup(client):
    await client.add_cog(Insider(client)) 