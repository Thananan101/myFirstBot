import discord
from discord.ext import commands
import random
import asyncio
import re
import json

class insider(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.active_timer = None
        self.vote_counts = {}
        self.vote_message = None
        self.players = {}
        self.vote_buttons = []  # Store the VoteBtn objects here
        self.player_votes = {}
        
    async def get_ids(self, user_id):
        if type(user_id) == list or type(user_id) == tuple:
            user_ids = [int(re.sub('[<>@!]', '', str(uid))) for uid in user_id]
        else:
            user_ids = int(re.sub('[<>@!]', '', str(user_id)))
        return user_ids
    
    async def get_member(self, user_id):
      user = await self.client.fetch_user(user_id)
      return user
        
    def get_word(self):
        with open('thai_words.json', 'r', encoding='utf-8') as file:
            content = json.load(file)

    
        word = random.choice(content)
        return word
    
    async def start_vote(self):
        if not self.vote_message:
            embed, view = self.get_embed_vote()
            self.vote_buttons = view.children  # Store the VoteBtn objects
            print(view.children)
            return embed, view
        else:
            await self.update_vote_count()


    @commands.Cog.listener()
    async def on_ready(self):
        print('insider is ready!')
    
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
        members = []
        mapped_list = list(zip(players, roles))

        for item in mapped_list:
            player = item[0]
            role = item[1]

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
            self.players[player.name] = {'player': player, 'role': role}
             
        for player_name in self.players:
            self.vote_counts[player_name] = 0  # Initialize vote count to 0 for each player
            
        async def timer_task():
            await ctx.send('เกมเริ่ม พวกคุณมีเวลา 5 นาที เลทสึโก') 
            await ctx.send('เริ่มจับเวลา')
            await asyncio.sleep(300) # 5 mins
            await ctx.send('จบเกมคับ 5 นาที')
            if not self.vote_message:
                embed, view = self.start_vote()
                self.vote_message = await ctx.send(embed=embed, view=view)
            else:
                await self.update_vote_count()
        
        self.active_timer = asyncio.create_task(timer_task())

    
    def get_embed_vote(self):
        embed = discord.Embed(
            title="Insider game",
            description="กดปุ่มโหวตคนที่คุณคิดว่าเป็นจอมบงการ (Insider)",
            color=int("1AA7EC", 16)
        )
        embed.set_thumbnail(url="https://github.com/alenros/insider/blob/master/public/ms-icon-144x144.png?raw=true")
        embed.add_field(name="Voting", value="Please cast your vote by clicking the button below.", inline=False)

        for player_name in self.players:

            embed.add_field(name=player_name, value=f"Votes: {self.vote_counts[player_name]}", inline=False)

        
        view = discord.ui.View()

        for player in self.players:

            vote_button = VoteBtn(self.players[player], self)
        
            view.add_item(vote_button)

        return embed, view
                
    @commands.command()
    async def vote(self, ctx):
        if not self.vote_message:
            embed, view = await self.start_vote()
            self.vote_message = await ctx.send(embed=embed, view=view)
        else:
            await self.update_vote_count()
    
    @commands.command()
    async def insider_ping(self, ctx):
        await ctx.send("insider pong!!")

    async def update_vote_count(self):
        # Retrieve the current click counters from the VoteBtn objects
        vote_counts = {player_name: button.click_counter for (player_name, _), button in zip(self.players.items(), self.vote_buttons)}
        
        # Update the vote_counts dictionary
        self.vote_counts = vote_counts

        embed, view = self.get_embed_vote()
        self.vote_buttons = view.children  # Store the VoteBtn objects
        await self.vote_message.edit(embed=embed, view=view)
        return embed, view
        
        
                    
    @commands.command()
    async def fs(self, ctx):
        if self.active_timer is None:
            await ctx.send("ไม่ได้มีการเล่นเกมอยู่คับ")
        else:
            self.active_timer.cancel()
            self.active_timer = None
            await ctx.send('มีคนใช้อำนาจหยุดเกม')
            embed, view = self.get_embed_vote()
            await self.vote_message.edit(embed=embed, view=view)
            

class VoteBtn(discord.ui.Button):
    def __init__(self, player, insider_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player
        self.insider_instance = insider_instance
        self.click_counter = insider_instance.vote_counts.get(self.player['player'].name, 0)


        # Set the button properties
        self.style = discord.ButtonStyle.primary
        self.label = f"{self.player['player'].name} (Clicks: {self.click_counter})"
        self.custom_id = f"vote_{str(self.player['player'].name)}"

    async def callback(self, interaction: discord.Interaction):
        print('callback')
        if self.player['player'].name in self.insider_instance.players and self.player['role'] != "HOST":
            try:
                previous_button = self.insider_instance.player_votes[self.player['player'].name]  # Get the previously voted button
            except:
                print('except')
                previous_button = None
            if previous_button is not None:
                label = self.insider_instance.player_votes[self.player['player'].name].label
                name = label.split(' ')[0]
                print(name)
                print(self.insider_instance.vote_counts)
                self.insider_instance.vote_counts[name] -= 1  # Deduct from the previous button's click counter
                print(self.insider_instance.vote_counts)
                previous_button.label = f"{name} (Clicks: {self.insider_instance.vote_counts[name]})"  # Update the label of the previous button

            self.insider_instance.player_votes[self.player['player'].name] = self  # Update the player's voted button
            print(self.insider_instance.player_votes[self.player['player'].name])
            print(type(self.insider_instance.player_votes[self.player['player'].name]))
            self.click_counter += 1  # Increment the click counter
            self.label = f"{self.player['player'].name} (Clicks: {self.click_counter})"  # Update the label with the new click count
            self.insider_instance.vote_counts[self.player['player'].name] += 1  # Update the vote count in the insider instance
            print(self.insider_instance.vote_counts)
            await interaction.response.defer()

            # Update the vote count in the insider instance
            await self.insider_instance.update_vote_count()
            print('---------------')
        else:
            await interaction.response.send_message("ผู้ดำเนินเกมกับคนที่ไม่เกี่ยวข้องอย่ายุ่งครับ.", ephemeral=True)

        

    
    
    
async def setup(client):
    await client.add_cog(insider(client))