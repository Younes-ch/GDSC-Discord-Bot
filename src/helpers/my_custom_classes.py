import asyncio
from discord.ext import commands
import html2text
import requests
import discord
import os

class MyButton(discord.ui.Button):
  def __init__(self, *, label, style, custom_id, emoji = None, disabled=False):
    super().__init__(label=label, style=style, custom_id=custom_id, emoji=emoji, disabled=disabled)

  async def callback(self, interaction: discord.Interaction):
    # ********************************************* Help Command *************************************************************
    if self.custom_id == 'next':
      self.view.current_page += 1
      if self.view.current_page == len(self.view.listOfEmbeds):
        self.view.current_page = 0
      await interaction.response.edit_message(embed=self.view.listOfEmbeds[self.view.current_page])
    elif self.custom_id == 'prev':
      self.view.current_page -= 1
      if self.view.current_page < 0:
        self.view.current_page = len(self.view.listOfEmbeds) - 1
      await interaction.response.edit_message(embed=self.view.listOfEmbeds[self.view.current_page])
    
    if len(self.view.children) > 1:
      if "Page" in self.view.children[1].label:
        self.view.children[1].label = 'Page: {}/{}'.format(self.view.current_page + 1, len(self.view.listOfEmbeds))
        await interaction.edit_original_response(embed=self.view.listOfEmbeds[self.view.current_page], view=self.view)

    # ********************************************* Question Command *************************************************************

    if self.custom_id in ['yes_most_upvoted_answer', 'no_most_upvoted_answer']:
      if interaction.user != self.view.interaction.user:
        await interaction.response.send_message('Only the author of the command can use this button.', ephemeral=True)
        await asyncio.sleep(1.0)
        await interaction.delete_original_response()
        return

    if self.custom_id == 'yes_most_upvoted_answer':
      await self.view.disable()
      data = requests.get(f'https://api.stackexchange.com/2.3/questions/{self.view.question_id}/answers?order=desc&sort=activity&site=stackoverflow&filter=3S33_h6y(QsUT2q4X').json()
      answers = [{ 
                  'up_vote_count': answer['up_vote_count'],
                  'down_vote_count': answer['down_vote_count'],
                  'body': self.view.converter.handle(answer['body']).strip(),
                  'title': answer['title'],
                  'link': answer['link'],
                  'owner': {
                    'display_name': answer['owner']['display_name'],
                    'link': answer['owner']['link'],
                    'profile_image': answer['owner']['profile_image']
                  }
                } for answer in data['items']]
      most_upvoted_answer = max(answers, key=lambda answer: answer['up_vote_count'])
      most_upvoted_answer_up_vote_count = most_upvoted_answer['up_vote_count']
      most_upvoted_answer_down_vote_count = most_upvoted_answer['down_vote_count']
      most_upvoted_answer_body = most_upvoted_answer['body']
      most_upvoted_answer_body = self.view.converter.handle(most_upvoted_answer_body).strip()
      most_upvoted_answer_title = most_upvoted_answer['title']
      most_upvoted_answer_link = most_upvoted_answer['link']
      most_upvoted_answer_owner = most_upvoted_answer['owner']['display_name']
      most_upvoted_answer_owner_link = most_upvoted_answer['owner']['link']
      most_upvoted_answer_owner_profile_image = most_upvoted_answer['owner']['profile_image']

      if len(most_upvoted_answer_body) > 1000:
        most_upvoted_answer_body = most_upvoted_answer_body[:900] + f'...\n\n[Read more]({most_upvoted_answer_link})'

      embed = discord.Embed(title=most_upvoted_answer_title, url=most_upvoted_answer_link, color=0x70e68a)
      embed.add_field(name='Answered by:', value=f'[**{most_upvoted_answer_owner}**]({most_upvoted_answer_owner_link})')
      embed.add_field(name='Upvotes:', value=most_upvoted_answer_up_vote_count)
      embed.add_field(name='Downvotes:', value=most_upvoted_answer_down_vote_count)
      embed.add_field(name='Answer:', value=most_upvoted_answer_body, inline=False)
      embed.set_thumbnail(url=most_upvoted_answer_owner_profile_image)
      embed.set_footer(text='Requested by {}'.format(interaction.user), icon_url=interaction.user.display_avatar.url)
      await interaction.response.send_message(embed=embed)

    elif self.custom_id == 'no_most_upvoted_answer':
      await interaction.response.send_message('Ok, I will not show the most upvoted answer.')
      await self.view.disable()

    # ********************************************* Rock Paper Scissors Command *************************************************************

    if self.custom_id in ('rock', 'scissors', 'paper'):
      self.view.players_choices.append(self.label)
      await self.view.disable()
      if interaction.user == self.view.author:
        await interaction.response.send_message(f'You chose **`{self.label}`**, Please wait for the other oponent to choose...')
        player2_msg = await self.view.member.send(f'You have been challenged by {self.view.author} to a game of **Rock Paper Scissors**!', embed=self.view.embed)
        self.view.player_msg = player2_msg
        await player2_msg.edit(view=self.view)
        await self.view.enable()
      else:
        await interaction.response.send_message(f'You chose **`{self.label}`**')
      if len(self.view.players_choices) == 2:
        await self.view.get_winner()
      
    # ********************************************* Slowmode Command *************************************************************

    if self.custom_id == 'yes_disable_slow_mode':
      await self.view.channel.edit(slowmode_delay=0)
      await self.view.interaction.edit_original_response(content='**⏱️ - Slowmode has been `disabled`.**', view=None)
      self.view.stop()
    elif self.custom_id == 'no_disable_slow_mode':
      await self.view.interaction.edit_original_response(content='**Okay, I will not disable slowmode.**', view=None)
      self.view.stop()

# ********************************************* Views *************************************************************
# ---------------------------------------------- Help Command View ------------------------------------------------
class ViewForHelpCommand(discord.ui.View):
  def __init__(self, *, interaction: discord.Interaction, listOfEmbeds : list[discord.Embed], timeout = 60):
    super().__init__(timeout=timeout)
    self.interaction = interaction
    self.listOfEmbeds = listOfEmbeds
    self.current_page = 0
    self.add_item(MyButton(label='Prev', style=discord.ButtonStyle.green, custom_id='prev'))
    self.add_item(MyButton(label='Page: {}/{}'.format(self.current_page + 1, len(self.listOfEmbeds)), style=discord.ButtonStyle.grey, custom_id='page', disabled=True))
    self.add_item(MyButton(label='Next', style=discord.ButtonStyle.green, custom_id='next'))

  async def on_timeout(self):
    self.children[0].disabled = True
    self.children[2].disabled = True
    await self.interaction.edit_original_response(embed=self.listOfEmbeds[self.current_page], view=self)

# ---------------------------------------------- Rock Paper Scissors Command View ------------------------------------------------
class ViewForRPSCommand(discord.ui.View):
  def __init__(self, *, interaction: discord.Interaction, author: discord.Member, member, player_msg: discord.Message, embed: discord.Embed, timeout = 30):
    super().__init__(timeout=timeout)
    self.interaction = interaction
    self.author = author
    self.member = member
    self.player_msg = player_msg
    self.embed = embed
    self.players_choices = []
    self.add_item(MyButton(label='🪨', style=discord.ButtonStyle.grey, custom_id='rock'))
    self.add_item(MyButton(label='🧻', style=discord.ButtonStyle.blurple, custom_id='paper'))
    self.add_item(MyButton(label='✂️', style=discord.ButtonStyle.red, custom_id='scissors'))

  async def on_timeout(self):
    self.children[0].disabled = True
    self.children[1].disabled = True
    self.children[2].disabled = True
    await self.interaction.edit_original_response(content=f'{self.author.mention}, {self.member.mention}: The game has ended due to inactivity!', embed=None)
    await self.player_msg.edit(view=self)

  async def disable(self):
    self.children[0].disabled = True
    self.children[1].disabled = True
    self.children[2].disabled = True
    await self.player_msg.edit(view=self)

  async def enable(self):
    self.children[0].disabled = False
    self.children[1].disabled = False
    self.children[2].disabled = False
    await self.player_msg.edit(view=self)

  async def get_winner(self):
    if self.players_choices[0] == '🪨' and self.players_choices[1] == '🧻':
      winner = self.member
    elif self.players_choices[0] == '🪨' and self.players_choices[1] == '✂️':
      winner = self.author
    elif self.players_choices[0] == '🧻' and self.players_choices[1] == '🪨':
      winner = self.author
    elif self.players_choices[0] == '🧻' and self.players_choices[1] == '✂️':
      winner = self.member
    elif self.players_choices[0] == '✂️' and self.players_choices[1] == '🪨':
      winner = self.member
    elif self.players_choices[0] == '✂️' and self.players_choices[1] == '🧻':
      winner = self.author
    elif self.players_choices[0] == self.players_choices[1]:
      winner = None

    if winner == None:
      embed = discord.Embed(title='Results', color=0xffffff)
      embed.add_field(name=f'{self.players_choices[0]} == {self.players_choices[1]}', value='**It\'s a Tie!**', inline=False)
      embed.set_author(name='Game Over!')
      embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6R63nEBSwQBGBICTHQrcbC9SAd_tdLR9k3w&usqp=CAU')
      embed.set_footer(text='Game made by Younes#5003', icon_url='https://cdn.discordapp.com/avatars/387798722827780108/788852766c106e9f8a88085a82651bd7.png?size=1024')
      await self.interaction.followup.send(embed=embed)
      await self.author.send(embed=embed)
      await self.member.send(embed=embed)
    elif winner == self.author:
        embed = discord.Embed(title='Results', color=self.author.top_role.color)
        embed.add_field(name=f'{self.players_choices[0]} > {self.players_choices[1]}', value=f'🥳 **{self.author.name}** Won! 🥳')
        embed.set_author(name='Game Over!')
        embed.set_thumbnail(url='https://www.pinclipart.com/picdir/big/576-5762132_player-1-wins-clipart.png')
        embed.set_footer(text='Game made by Younes#5003', icon_url='https://cdn.discordapp.com/avatars/387798722827780108/788852766c106e9f8a88085a82651bd7.png?size=1024')
        await self.interaction.followup.send(embed=embed)
        await self.author.send(embed=embed)
        await self.member.send(embed=embed)
    else:
        embed = discord.Embed(title='Results', color=self.member.top_role.color)
        embed.add_field(name=f'{self.players_choices[1]} > {self.players_choices[0]}', value=f'🥳 **{self.member.name}** Won! 🥳')
        embed.set_author(name='Game Over!')
        embed.set_thumbnail(url='http://learnlearn.uk/scratch/wp-content/uploads/sites/7/2018/01/player2png.png')
        embed.set_footer(text='Game made by Younes#5003', icon_url='https://cdn.discordapp.com/avatars/387798722827780108/788852766c106e9f8a88085a82651bd7.png?size=1024')
        await self.interaction.followup.send(embed=embed)
        await self.author.send(embed=embed)
        await self.member.send(embed=embed)
    self.players_choices.clear()
    self.stop()

# --------------------------------------------------- StackOverflow Question Select Menu --------------------------------------------------- #
class SelectStackOverflowQuestion(discord.ui.Select):
  def __init__(self, interaction: discord.Interaction, questions : list[str], questions_id : list[int], converter : html2text.HTML2Text):
    mapping = {
      1: "1️⃣",
      2: "2️⃣",
      3: "3️⃣",
      4: "4️⃣",
      5: "5️⃣",
    }
    options = [
      discord.SelectOption(label=question, value=questions_id[questions.index(question)], 
      emoji=discord.PartialEmoji(name= mapping[i+1])) for i, question in enumerate(questions)
    ]
    super().__init__(placeholder="Select a question", min_values=1, max_values=1, options=options)
    self.API_KEY = os.getenv('STACKOVERFLOW_API_KEY')
    self.interaction = interaction
    self.converter = converter

  async def callback(self, interaction: discord.Interaction):
    if interaction.user != self.interaction.user:
      await interaction.response.send_message("Only who invoked the command can choose a question!", ephemeral=True)
      await asyncio.sleep(1.5)
      await interaction.delete_original_response()
      return
    question_id = self.values[0]
    response = requests.get(f"https://api.stackexchange.com/2.3/questions/{question_id}?order=desc&sort=activity&site=stackoverflow")
    data = response.json()

    if data["items"]:
      question = data['items'][0]['title']
      if data["items"][0]["answer_count"] == 0:
        await interaction.response.send_message(f'The question: **{question}** has no answers yet.', ephemeral=True)
        await self.view.disable()
        return
      top_answer_id = data["items"][0].get("accepted_answer_id", None)

      if top_answer_id:
        full_response = requests.get(f"https://api.stackexchange.com/2.2/answers/{top_answer_id}?order=desc&sort=votes&site=stackoverflow&filter=3S33_h6y(QsUT2q4X&key={self.API_KEY}")
        full_data = full_response.json()
        question = full_data["items"][0]["title"]
        answer = full_data["items"][0]["body"]
        answer_owner_name = f"{full_data['items'][0]['owner']['display_name']}"
        answer_owner_avatar = full_data["items"][0]["owner"]["profile_image"]
        answer_owner_profile_link = full_data["items"][0]["owner"]["link"]
        answer_link = full_data["items"][0]["link"]
        answer_up_vote_count = full_data["items"][0]["up_vote_count"]
        answer_down_vote_count = full_data["items"][0]["down_vote_count"]

        markdown_answer = self.converter.handle(answer).strip()
        if len(markdown_answer) > 1000:
          markdown_answer = markdown_answer[:800] + f"...\n\n[Read more]({answer_link})"

        embed = discord.Embed(title=question, url=answer_link, color=0x00ff00)
        embed.add_field(name="Answered by", value=f"[{answer_owner_name}]({answer_owner_profile_link})")
        embed.add_field(name="Upvotes", value=answer_up_vote_count)
        embed.add_field(name="Downvotes", value=answer_down_vote_count)
        embed.add_field(name="Answer:", value=markdown_answer)
        embed.set_thumbnail(url=answer_owner_avatar)
        embed.set_footer(text='Requested by {}'.format(self.interaction.user), icon_url=self.interaction.user.display_avatar.url)
        await interaction.response.send_message("Here is the accepted answer to your question:", embed=embed)
      else:
        view = ViewForYesOrNoMostUpvotedAnswer(interaction, question_id, self.converter)
        await interaction.response.send_message(content=f"I'm sorry, there is no accepted answer to the question: **{question}** on Stack Overflow.\n{self.interaction.user.mention} **Do you want to get the most upvoted answer?**", view=view)
    else:
      await interaction.response.send_message(content=f"I'm sorry, I could not find any answers to the question: **{question}** on Stack Overflow.", ephemeral=True)
    await self.view.disable()


# --------------------------------------------------- Question Command View --------------------------------------------------- #
class ViewForQuestionCommand(discord.ui.View):
  def __init__(self, interaction : discord.Interaction, questions : list[str], questions_id : list[int], converter : html2text.HTML2Text, timeout = 15):
    super().__init__(timeout=timeout)
    self.interaction = interaction
    self.add_item(SelectStackOverflowQuestion(interaction, questions, questions_id, converter))    

  async def disable(self):
    await self.interaction.delete_original_response()
    self.stop()

  async def on_timeout(self):
    await self.interaction.edit_original_response(content=f"{self.interaction.user.mention} You took too long to select a question. Please try again.", view=None)
    await asyncio.sleep(10)
    await self.interaction.delete_original_response()
    self.stop()

# --------------------------------------------------- Yes or No Most Upvoted Answer View --------------------------------------------------- #
class ViewForYesOrNoMostUpvotedAnswer(discord.ui.View):
  def __init__(self, interaction: discord.Interaction, question_id : int, converter : html2text.HTML2Text, timeout = 30):
    super().__init__(timeout=timeout)
    self.interaction = interaction
    self.question_id = question_id
    self.converter = converter
    self.add_item(MyButton(label="Yes", style=discord.ButtonStyle.green, custom_id="yes_most_upvoted_answer", emoji="✅"))
    self.add_item(MyButton(label="No", style=discord.ButtonStyle.red, custom_id="no_most_upvoted_answer", emoji="❌"))

  async def disable(self):
    self.children[0].disabled = True
    self.children[1].disabled = True
    await self.interaction.edit_original_response(view=self)
    self.stop()

  async def delete(self):
    await self.interaction.delete_original_response()
    self.stop()

  async def on_timeout(self):
    self.children[0].disabled = True
    self.children[1].disabled = True
    await self.interaction.edit_original_response(content=f"{self.interaction.user.mention} You took too long to select an option. Please try again.", view=None)
    await asyncio.sleep(10)
    await self.delete()

# --------------------------------------------------- Social Media Command View --------------------------------------------------- #
class ViewForSocialMediaCommand(discord.ui.View):
  def __init__(self, bot: commands.Bot):
    super().__init__(timeout=None)
    self.google_emoji = bot.get_emoji(1057434239261491200)
    self.facebook_emoji = bot.get_emoji(1057425555856822373)
    self.instagram_emoji = bot.get_emoji(1057432580661706813)
    self.youtube_emoji = bot.get_emoji(1057432578665226271)
    self.spotify_emoji = bot.get_emoji(1057432573611094096)
    self.spotify_url = 'https://open.spotify.com/show/3wrC7hOR6OIImXuEkMqmPm?go=1&sp_cid=5a981dbb5ad7e10879beed6ba2664cca&utm_source=embed_player_p&utm_medium=desktop&nd=1'
    self.linkedin_emoji = bot.get_emoji(1057432575213305887)
    self.twitter_emoji = bot.get_emoji(1057432577037828137)
    self.apple_emoji = bot.get_emoji(1057432511757684767)
    self.add_item(discord.ui.Button(
                                label='GDSC Platform',
                                url='https://gdsc.community.dev/higher-institute-of-applied-science-and-technology/', emoji=self.google_emoji, row=0)
                            )
    self.add_item(discord.ui.Button(label='Facebook', url='https://www.facebook.com/GDSC.ISSATSo/', emoji=self.facebook_emoji, row=0))
    self.add_item(discord.ui.Button(label='Instagram', url='https://www.instagram.com/gdsc.issatso/', emoji=self.instagram_emoji, row=0))
    self.add_item(discord.ui.Button(label='YouTube', url='https://www.youtube.com/@googledeveloperstudentclub7820', emoji=self.youtube_emoji, row=0))
    self.add_item(discord.ui.Button(label='LinkedIn', url='https://www.linkedin.com/company/gdsc-issatso/', emoji=self.linkedin_emoji, row=1))
    self.add_item(discord.ui.Button(label='Twitter', url='https://twitter.com/GDSC_ISSATSO', emoji=self.twitter_emoji, row=1))
    self.add_item(discord.ui.Button(label='E-mail', url="https://mailto:dscissatso@gmail.com", emoji="📧", row=1))
    self.add_item(discord.ui.Button(label='Spotify', url=self.spotify_url, emoji=self.spotify_emoji, row=2))
    self.add_item(discord.ui.Button(label='Apple Podcasts', url='https://podcasts.apple.com/us/podcast/gdsc-podcast/id1569890008', emoji=self.apple_emoji, row=2))

# --------------------------------------------------- Yes or No Disable Slow Mode View --------------------------------------------------- #
class ViewForYesOrNoDisableSlowMode(discord.ui.View):
  def __init__(self, interaction: discord.Interaction, channel: discord.TextChannel):
    super().__init__(timeout=30)
    self.interaction = interaction
    self.channel = channel
    self.add_item(MyButton(label="Yes", style=discord.ButtonStyle.green, custom_id="yes_disable_slow_mode", emoji="✅"))
    self.add_item(MyButton(label="No", style=discord.ButtonStyle.red, custom_id="no_disable_slow_mode", emoji="❌"))
  
  async def delete(self):
    await self.interaction.delete_original_response()
    self.stop()
  
  async def on_timeout(self):
    self.children[0].disabled = True
    self.children[1].disabled = True
    await self.interaction.edit_original_response(content=f"{self.interaction.user.mention} You took too long to select an option. Please try again.", view=None)
    await asyncio.sleep(10)
    await self.delete()