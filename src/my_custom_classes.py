from discord.ext import commands
import html2text
import requests
import discord
import os

class MyButton(discord.ui.Button):
  def __init__(self, *, label, style, custom_id, emoji = None, disabled=False):
    super().__init__(label=label, style=style, custom_id=custom_id, emoji=emoji, disabled=disabled)

  async def callback(self, interaction: discord.Interaction):
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
    
    if "Page" in self.view.children[1].label:
      self.view.children[1].label = 'Page: {}/{}'.format(self.view.current_page + 1, len(self.view.listOfEmbeds))
      await interaction.message.edit(view=self.view)

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

      embed = discord.Embed(title=most_upvoted_answer_title, color=0x70e68a)
      embed.add_field(name='Answered by:', value=f'[**{most_upvoted_answer_owner}**]({most_upvoted_answer_owner_link})')
      embed.add_field(name='Upvotes:', value=most_upvoted_answer_up_vote_count)
      embed.add_field(name='Downvotes:', value=most_upvoted_answer_down_vote_count)
      embed.add_field(name='Answer:', value=most_upvoted_answer_body, inline=False)
      embed.set_thumbnail(url=most_upvoted_answer_owner_profile_image)
      embed.set_footer(text='Requested by {}'.format(interaction.user), icon_url=interaction.user.display_avatar.url)
      await interaction.response.send_message(embed=embed)

    elif self.custom_id == 'no_most_upvoted_answer':
      await interaction.response.send_message('Ok, I will not show the most upvoted answer.', ephemeral=True)
      await self.view.disable()

    if self.custom_id == 'rock' or self.custom_id == 'scissors' or self.custom_id == 'paper':
      await interaction.response.send_message('You chose **`{}`**, Please wait for the other oponent to choose...'.format(self.label))
      self.view.players_choices.append(self.label)
      await self.view.disable()
      if interaction.user == self.view.author:
        player2_msg = await self.view.member.send(embed=self.view.embed)
        self.view.player_msg = player2_msg
        await player2_msg.edit(view=self.view)
        await self.view.enable()
      if len(self.view.players_choices) == 2:
        await self.view.get_winner()


class ViewForHelpCommand(discord.ui.View):
  def __init__(self, *, message, listOfEmbeds : list[discord.Embed], timeout = 30):
    super().__init__(timeout=timeout)
    self.message = message
    self.listOfEmbeds = listOfEmbeds
    self.current_page = 0
    self.add_item(MyButton(label='Prev', style=discord.ButtonStyle.green, custom_id='prev'))
    self.add_item(MyButton(label='Page: {}/{}'.format(self.current_page + 1, len(self.listOfEmbeds)), style=discord.ButtonStyle.grey, custom_id='page', disabled=True))
    self.add_item(MyButton(label='Next', style=discord.ButtonStyle.green, custom_id='next'))

  async def on_timeout(self):
    self.children[0].disabled = True
    self.children[2].disabled = True
    await self.message.edit(view=self)

class ViewForRPSCommand(discord.ui.View):
  def __init__(self, *, ctx, author, message, member, player_msg, embed, timeout = 30):
    super().__init__(timeout=timeout)
    self.ctx = ctx
    self.author = author
    self.message = message
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
    await self.ctx.send('{}, {}: The game has ended due to inactivity!'.format(self.ctx.author.mention, self.member.mention))
    await self.player_msg.delete()

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
      embed = discord.Embed(title='Results', color=self.author.top_role.color)
      embed.add_field(name=f'{self.players_choices[0]} == {self.players_choices[1]}', value='**It\'s a Tie!**', inline=False)
      embed.set_author(name='Game Over!')
      embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6R63nEBSwQBGBICTHQrcbC9SAd_tdLR9k3w&usqp=CAU')
      embed.set_footer(text='Game made by Younes#5003', icon_url='https://cdn.discordapp.com/avatars/387798722827780108/788852766c106e9f8a88085a82651bd7.png?size=1024')
      await self.message.delete()
      await self.ctx.send(embed=embed)
      await self.author.send(embed=embed)
      await self.member.send(embed=embed)
    elif winner == self.author:
        embed = discord.Embed(title='Results', color=self.author.top_role.color)
        embed.add_field(name=f'{self.players_choices[0]} > {self.players_choices[1]}', value=f'🥳 **{self.author.name}** Won! 🥳')
        embed.set_author(name='Game Over!')
        embed.set_thumbnail(url='https://www.pinclipart.com/picdir/big/576-5762132_player-1-wins-clipart.png')
        embed.set_footer(text='Game made by Younes#5003', icon_url='https://cdn.discordapp.com/avatars/387798722827780108/788852766c106e9f8a88085a82651bd7.png?size=1024')
        await self.message.delete()
        await self.ctx.send(embed=embed)
        await self.author.send(embed=embed)
        await self.member.send(embed=embed)
    else:
        embed = discord.Embed(title='Results', color=self.author.top_role.color)
        embed.add_field(name=f'{self.players_choices[1]} > {self.players_choices[0]}', value=f'🥳 **{self.member.name}** Won! 🥳')
        embed.set_author(name='Game Over!')
        embed.set_thumbnail(url='http://learnlearn.uk/scratch/wp-content/uploads/sites/7/2018/01/player2png.png')
        embed.set_footer(text='Game made by Younes#5003', icon_url='https://cdn.discordapp.com/avatars/387798722827780108/788852766c106e9f8a88085a82651bd7.png?size=1024')
        await self.message.delete()
        await self.ctx.send(embed=embed)
        await self.author.send(embed=embed)
        await self.member.send(embed=embed)
    self.players_choices.clear()
    self.stop()

class SelectStackOverflowQuestion(discord.ui.Select):
  def __init__(self, ctx : commands.Context, questions : list[str], questions_id : list[int], converter : html2text.HTML2Text):
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
    self.ctx = ctx
    self.converter = converter

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.send_message("Loading...", ephemeral=True)
    question_id = self.values[0]
    response = requests.get(f"https://api.stackexchange.com/2.3/questions/{question_id}?order=desc&sort=activity&site=stackoverflow")
    data = response.json()

    if data["items"]:
      if data["items"][0]["answer_count"] == 0:
        await interaction.edit_original_response(content="This question has no answers yet.")
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
          markdown_answer = markdown_answer[:900] + f"...\n\n[Read more]({answer_link})"

        embed = discord.Embed(title=question, color=0x00ff00)
        embed.add_field(name="Answered by", value=f"[{answer_owner_name}]({answer_owner_profile_link})")
        embed.add_field(name="Upvotes", value=answer_up_vote_count)
        embed.add_field(name="Downvotes", value=answer_down_vote_count)
        embed.add_field(name="Answer:", value=markdown_answer)
        embed.set_thumbnail(url=answer_owner_avatar)
        embed.set_footer(text='Requested by {}'.format(interaction.user), icon_url=interaction.user.display_avatar.url)
        await interaction.edit_original_response(content="Here is the accepted answer to your question:", embed=embed)
      else:
        await interaction.edit_original_response(content="I'm sorry, there is no accepted answer to that question on Stack Overflow.")
        message = await self.ctx.send("**Do you want to get the most upvoted answer?**")
        view = ViewForYesOrNoMostUpvotedAnswer(self.ctx, question_id, message, self.converter)
        await message.edit(view=view)
    else:
      await interaction.edit_original_response(content="I'm sorry, I could not find any answers to that question on Stack Overflow.")
    self.view.stop()

class ViewForQuestionCommand(discord.ui.View):
  def __init__(self, ctx : commands.Context, questions : list[str], questions_id : list[int], converter : html2text.HTML2Text):
    super().__init__()
    self.add_item(SelectStackOverflowQuestion(ctx, questions, questions_id, converter))

class ViewForYesOrNoMostUpvotedAnswer(discord.ui.View):
  def __init__(self, ctx : commands.Context, question_id : int, message : discord.Message, converter : html2text.HTML2Text, timeout = 15):
    super().__init__(timeout=timeout)
    self.ctx = ctx
    self.question_id = question_id
    self.message = message
    self.converter = converter
    self.add_item(MyButton(label="Yes", style=discord.ButtonStyle.green, custom_id="yes_most_upvoted_answer", emoji="✅"))
    self.add_item(MyButton(label="No", style=discord.ButtonStyle.red, custom_id="no_most_upvoted_answer", emoji="❌"))

  async def disable(self):
    self.children[0].disabled = True
    self.children[1].disabled = True
    await self.message.edit(view=self)
    self.stop()

  async def on_timeout(self):
    await self.disable()