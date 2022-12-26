from PIL import Image, ImageFont, ImageDraw
from my_custom_functions import *
from discord import app_commands
from discord.ext import commands
from my_custom_classes import *
from dotenv import load_dotenv
from discord.ext import tasks
import urllib.parse
import html2text
import discord
import requests
import discord
import logging
import asyncio
import json
import os

load_dotenv()
intents = discord.Intents.all()
logging.basicConfig(level=logging.INFO)
activity = discord.Activity(type=discord.ActivityType.listening, name="/help")
bot = commands.Bot(command_prefix='&', intents=intents, activity=activity)
bot.remove_command('help')

@bot.event
async def on_ready():
  print('------')
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print('------')
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s):")
    for command in synced:
      print('\033[33m', command.name, '\33[0m-->', command.description)
  except Exception as e:
    print(e)
  member_count.start()
  for guild in bot.guilds:
    if not guild.id in [828940910053556224, 783404400416391189]:
      await guild.owner.send(':rolling_eyes: Sorry, I left `{}` because I\'m a private bot that only works in `GDSC ISSATSo Community Server!`'.format(guild.name))
      await guild.leave()
    else:
      invites[guild.id] = await guild.invites()

# -------------------------------------- Bot commands -------------------------------------- #

cmds = [
  {
    'name' : '/avatar',  
    'args' : ['[member]', ''],
    'exmp' : ['/avatar @user', '/avatar'],
    'dis' : 'Returns the avatar of the member mentioned or the user who invoked the command (in case no one was mentioned).'
  },
  {
    'name': '/icon',
    'args': [''],
    'exmp': ['/icon'],
    'dis': 'Returns the server icon.'
  },
  {
    'name' : '/meme',  
    'args' : ['[subreddit name]', ''],
    'exmp': ['/meme dankmemes', '/meme'],
    'dis' : 'Returns a random meme from the subbredit you provided or Dankmemes/memes/me_irl (in case no Subbredit name was provided).'
  },
  { 
    'name' : '/weather',  
    'args' : ['[city name]', ''],
    'exmp' : ['/weather Monastir', '/weather'],
    'dis' : 'Returns current weather in the city mentioned or Sousse if no city was mentioned.'
  },
  {
    'name' : '/say',
    'args' : ['[Text Channel] [message]', '[message]'],
    'exmp': ['/say #general Hello everyone!', '/say Hello everyone!'],
    'dis' : 'Sends the message as the bot in the text channel provided.'
  },
  {
    'name': '&announce',
    'args': ['[message]'],
    'exmp': '&announce Hello everyone!',
    'exmp': ['&announce Hello everyone!'],
    'dis': 'Sends the message as the bot in the announcements channel.'
  },
  {
    "name" : '/fact', 
    'args' : [''],
    'exmp': ['/fact'],
    'dis' : 'Returns a random fact.'
  },
  {
    "name" : '/corona', 
    'args' : ['[country name]', ''],
    'exmp': ['/corona morocco', '/corona'],
    'dis' : 'Returns today''s COVID-19 statistics of the mentioned country (Tunisia if none was mentioned).'
  },
  {
    "name" : '/snipe',  
    'args' : [''],
    'exmp': ['/snipe'],
    'dis' : 'Returns last deleted messages in the channel where the command was called.'
  },
  {
    "name" : '/rps', 
    'args' : ['[member]'],
    'exmp': ['/rps @user'],
    'dis' : 'Creates a RPS game between you and the mentioned member.'
  },
  {
    "name" : '/joke', 
    'args' : ['[word]', ''],
    'exmp': ['/joke', '/joke programming'],
    'dis' : 'Returns a random joke contains the word (word argument can be omitted).'
  },
  {
    "name" : '/ping', 
    'args' : [''],
    'exmp': ['/ping'],
    'dis' : 'Returns current bot\'s ping.'
  },
  {
    "name" : '/quote', 
    'args' : [''],
    'exmp': ['/quote'],
    'dis' : 'Returns a random quote.'
  },
  {
    "name" : '/userinfo', 
    'args' : ['[member]', ''],
    'exmp': ['/userinfo @user', '/userinfo'],
    'dis' : 'Shows detailed information about the mentioned member or the user in case no one was mentioned.'
  },
  {
    "name" : '/serverinfo', 
    'args' : [''],
    'exmp': ['/serverinfo'],
    'dis' : 'Shows detailed information about the server where the command was called.'
  },
  {
    "name" : "/question",
    "args" : ["[question]"],
    'exmp': ['/question How to center a div?'],
    "dis" : "Fetches a similar question from stackoverflow and returns the correct answer."
  },
  {
    "name" : '/help', 
    'args' : ['[command]', ''],
    'exmp': ['/help', '/help avatar'],
    'dis' : 'Returns the list of all commands or get help for a specific command.'
  }
]

# ------------------------------------- Help command ------------------------------------------- #

#help command
@bot.tree.command(description='Get the list of all commands or get help for a specific command.')
@app_commands.choices(choices=[app_commands.Choice(name=cmd['name'], value=cmd['name']) for cmd in cmds])
async def help(interaction: discord.Interaction, choices: app_commands.Choice[str] | None):
  if choices is None:
    embed1 = discord.Embed(title='Commands:', color=0x70e68a)
    embed2 = discord.Embed(title='Commands:', color=0x70e68a)
    embed3 = discord.Embed(title='Commands:', color=0x70e68a)
    embed4 = discord.Embed(title='Commands:', color=0x70e68a)
    embed1.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
    embed1.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
    embed2.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
    embed2.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
    embed3.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
    embed3.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
    embed4.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
    embed4.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
    counter = 0
    for cmd in cmds:
      counter += 1
      if counter <= 5:
        embed1.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
      elif counter > 5 and counter <= 10:
        embed2.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
      elif counter > 11 and counter <= 16:
        embed3.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
      else:
        embed4.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
    listOfEmbeds = [embed1, embed2, embed3, embed4]
    await interaction.response.send_message(embed=embed1, ephemeral=True)
    view = ViewForHelpCommand(interaction=interaction, listOfEmbeds=listOfEmbeds)
    await interaction.edit_original_response(view=view)
  else:
    for cmd in cmds:
      if cmd['name'] == choices.name:
        embed = generate_embed(cmd['name'].capitalize(), cmd['dis'], interaction.user, {'usage' : [f'{cmd["name"]} {arg}' for arg in cmd['args']], 'examples' : cmd["exmp"]})
        await interaction.response.send_message(embed=embed, ephemeral=True)
        break

# ----------------------------------------- Events -------------------------------------------------

@tasks.loop(seconds=30.0)
async def member_count():
  for guild in bot.guilds:
    overwrites = {
      guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False)
    }
    found = False
    for vc in guild.voice_channels:
      if vc.name.lower().startswith('member count:'):
        await vc.edit(name='Member count: {}'.format(guild.member_count), overwrites=overwrites, user_limit=0, position=0)
        found = True
        break
    if not found:
      await guild.create_voice_channel(name='Member count: {}'.format(guild.member_count), overwrites=overwrites, position=0, user_limit=0)
  print('Updated')

@bot.event
async def on_member_update(before, after):
  before_roles = [role.name for role in before.roles]
  after_roles = [role.name for role in after.roles]
  if "Event Speaker" not in before_roles and "Event Speaker" in after_roles:
    if "Event Speaker" not in after.display_name:
      try:
        await after.edit(nick=f'[Event Speaker] {before.display_name}')
      except discord.errors.Forbidden:
        await after.send('**Event Speaker** Role has just been __added__ to your roles in **{}** server, please go ahead and add **[Event Speaker]** *tag* to your nickname'.format(after.guild.name))
  elif "Event Speaker" in before_roles and "Event Speaker" not in after_roles:
    if "[Event Speaker]" in after.display_name:
      try:
        await after.edit(nick=after.display_name.replace("[Event Speaker] ", ""))
      except discord.errors.Forbidden:
        await after.send('**Event Speaker** Role has just been __removed__ from your roles in **{}** server, please go ahead and remove **[Event Speaker]** *tag* from your nickname'.format(after.guild.name))

invites = {}

@bot.event
async def on_member_join(member):
  if member.guild.id == 828940910053556224:
    welcome_channel = bot.get_channel(935969094652551189)
    invites_channel = bot.get_channel(940729129689554944)
  else:
    welcome_channel = bot.get_channel(783406528165838888)
    rules_channel = bot.get_channel(841102973206659134)
    invites_channel = bot.get_channel(941418127261040720)
    await rules_channel.send(member.mention, delete_after=0.1)
    await member.add_roles(member.guild.get_role(835557953057718314), reason="New Member")

  if not member.bot:
    avatar_file_name = "avatar.png"
    await member.display_avatar.save(avatar_file_name)
    avatar = Image.open("avatar.png")
    avatar = avatar.resize((148, 140))

    mask_im = Image.new("L", avatar.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0, 0, 148, 140), fill=255, outline=0, width=2)
    mask_im.save('mask_circle.png', quality=95)

    background = Image.open('src/Assets/GDSC Welcome Template.png')
    font = ImageFont.truetype("src/Assets/Google-Sans.ttf", 54)
    background_copy = background.copy()
    background_copy.paste(avatar, (951, 596), mask_im)
    draw = ImageDraw.Draw(background_copy)
    margin = 410 if len(member.display_name) == 2 else (410 - ((len(member.display_name)/2) * 20))
    draw.text((margin, 407), '{}'.format(member.display_name), (231, 245, 254), font=font)
    
    background_copy.save("member_landed.png")

    await welcome_channel.send(content=f'Welcome {member.mention} to **GDSC ISSATSo Community Server**. *Enjoy your stay!*', file=discord.File("member_landed.png"))
    await asyncio.sleep(1)
    os.remove("member_landed.png")
    os.remove("avatar.png")
    os.remove('mask_circle.png')

  global invites
  invites_before_join = invites[member.guild.id]
  invites_after_join = await member.guild.invites()

  for invite in invites_before_join:
    if find_invite_by_code(invites_after_join, invite.code):
      if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
        embed = discord.Embed(description='📥 **{} has joined the server**'.format(member.mention), color=0x6BF2E4)
        embed.set_author(name=f'{member.name}', icon_url=member.display_avatar.url)
        embed.add_field(name='🔒 Invite Code:', value=invite.code)
        embed.add_field(name='✉️ Inviter:', value=invite.inviter)
        embed.set_footer(text='Guild: {}'.format(member.guild.name), icon_url=member.guild.icon.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        await asyncio.sleep(2)
        await invites_channel.send(embed=embed)
        invites[member.guild.id] = invites_after_join

@bot.event
async def on_member_remove(member):
  invites[member.guild.id] = await member.guild.invites()

@bot.event
async def on_guild_join(guild):
  if not guild.id in [828940910053556224, 783404400416391189]:
    await guild.owner.send(':rolling_eyes: Sorry, i left `{}` because i\'m a private bot that only works in `GDSC ISSATSo Community Server!`'.format(guild.name))
    await guild.leave()

last_msg = []

@bot.event
async def on_message_delete(message):
  global last_msg
  if not message.author.bot:
    last_msg.append(message)
  await asyncio.sleep(60)
  if len(last_msg) > 10:
    last_msg.clear()

# -------------------------------------------- Commands --------------------------------------------

# rps command
@bot.tree.command(description='Play Rock Paper Scissors with your friends!')
async def rps(interaction: discord.Interaction, member : discord.Member):
  if interaction.user == member or member.bot:
    raise app_commands.AppCommandError()
  else:
    await interaction.response.defer(thinking=True)
    embed = discord.Embed(title='Rock Paper Scissors:', description='**Who will win? 🤔**', color=interaction.user.top_role.color)
    embed.set_thumbnail(url='https://facts.net/wp-content/uploads/2020/11/rock-paper-scissors.jpg')
    embed.add_field(name='Player 1:', value=interaction.user.name)
    embed.add_field(name='Player 2:', value=member.name)
    await interaction.followup.send(embed=embed)
    embed.description = '**Choose an option from below:**'
    player1_msg = await interaction.user.send(f'You challenged **{member.name}** to a game of **Rock Paper Scissors**!', embed=embed)
    view = ViewForRPSCommand(interaction=interaction, author=interaction.user, member=member, player_msg=player1_msg, embed=embed)
    await player1_msg.edit(view=view)

# question command
@bot.tree.command(description='Get the best answer to your question from StackOverflow!')
async def question(interaction: discord.Interaction, question: str):
  # {
  #   "My Test Server ID": "ID",
  #   "GDSC ISSATSo Community Server ID": "ID",
  # }
  corresponding_channels = {
    828940910053556224: 1055489016281182360,
    783404400416391189: 1056268271323709451,
  }
  question = '"' + urllib.parse.quote(question.lower()) + '"'
  API_KEY = os.getenv('STACKOVERFLOW_API_KEY')
  if interaction.channel.id in corresponding_channels.values():
    response = requests.get(f"https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q={question}&site=stackoverflow&key={API_KEY}")
    data = response.json()

    converter = html2text.HTML2Text()

    if data["items"]:
      questions = []
      questions_id = []
      for i in range(min(5, len(data["items"]))):
        question_title = converter.handle(data["items"][i]["title"]).strip()[:97] + "..."
        questions.append(question_title)
        questions_id.append(data["items"][i]["question_id"])
      view = ViewForQuestionCommand(interaction, questions, questions_id, converter)
      await interaction.response.defer()
      await interaction.followup.send(f"Here are the top 5 similar questions that I found on Stack Overflow:", view=view)
    else:
      await interaction.response.send_message("I'm sorry, I could not find any similar posted question to that question on Stack Overflow.")
  else:
    await interaction.response.send_message(f"Please use this command in the <#{corresponding_channels[interaction.guild.id]}> channel.", ephemeral=True)
    return

@question.error
async def question_error(ctx : commands.Context, error: commands.CommandError):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(title='Missing Arguments Error', description=':no_entry: - You are missing the required arguments to run this command!', color=0xe74c3c)
    embed.add_field(name='Command:', value='**&question `[question]`**')
    await ctx.send(embed=embed)
  else:
    print(error)

# Server Info Command
@bot.tree.command(name='serverinfo', description='Get the server info')
async def server_info(interaction: discord.Interaction):
  statuses_count = {
    'online': sum(1 for m in interaction.guild.members if m.status.name == 'online'),
    'idle': sum(1 for m in interaction.guild.members if m.status.name == 'idle'),
    'dnd': sum(1 for m in interaction.guild.members if m.status.name == 'dnd'),
    'offline': sum(1 for m in interaction.guild.members if m.status.name == 'offline')
  }
  guild_name =interaction.guild.name
  guild_text_channels = len(interaction.guild.text_channels)
  guild_voice_channels = len(interaction.guild.voice_channels)
  guild_categories = len(interaction.guild.categories)
  guild_member_count = interaction.guild.member_count
  guild_human_members = len([x for x in interaction.guild.members if not x.bot])
  guild_bot_members = guild_member_count - guild_human_members
  guild_banned_members = len([entry async for entry in interaction.guild.bans(limit=2000)])
  guild_member_statuses = f'🟢 {statuses_count["online"]} | 🟠 {statuses_count["idle"]} | ⛔ {statuses_count["dnd"]} | ⚪ {statuses_count["offline"]}'
  guild_roles_count = len(interaction.guild.roles)
  guild_highest_role = interaction.guild.roles[-1].mention
  guild_description = interaction.guild.description if interaction.guild.description else 'N/A'
  footer_text ='Guild ID: {} • Created at: {}'.format(interaction.guild.id, interaction.guild.created_at.strftime("%d-%b-%Y"))
  embed = discord.Embed(title='Server information', color=interaction.user.top_role.color)
  embed.add_field(name='Name:', value=guild_name)
  embed.add_field(name='Avatar:', value="[Click Here]({})".format(interaction.guild.icon.url))
  embed.add_field(name='Members:', value=guild_member_count)
  embed.add_field(name='Humans:', value=guild_human_members)
  embed.add_field(name='Bots:', value=guild_bot_members)
  embed.add_field(name='Banned:', value=guild_banned_members)
  embed.add_field(name='Statuses:', value=guild_member_statuses)
  embed.add_field(name='Text channels:', value=guild_text_channels)
  embed.add_field(name='Voice channels:', value=guild_voice_channels)
  embed.add_field(name='Categories:', value=guild_categories)
  embed.add_field(name='Roles:', value=guild_roles_count)
  embed.add_field(name='Highest Role:', value=f'{guild_highest_role}')
  embed.add_field(name='Invites:', value=len(await interaction.guild.invites()))
  embed.add_field(name='Description:', value=guild_description, inline=False)
  embed.set_thumbnail(url=interaction.guild.icon.url)
  embed.set_footer(text=footer_text)
  await interaction.response.send_message(embed=embed, ephemeral=True)

# User info command
@bot.tree.command(name='userinfo', description='Display information about a user')
async def user_info(interaction: discord.Interaction, member : discord.Member = None):
  statuses = {
    'online' : '🟢 Online',
    'idle' : '🟠 Idle',
    'dnd' : '⛔ Do not Disturb',
    'offline' : '⚪ Offline',
  }
  if not member:
    member = interaction.user
  guild = interaction.guild
  status = statuses[guild.get_member(member.id).status.name]
  embed = discord.Embed(title='User information:', color = member.top_role.color)
  embed.add_field(name='Name', value=member)
  embed.add_field(name='ID', value=member.id)
  embed.add_field(name='Status', value=status)
  embed.add_field(name='Bot?', value='✅' if member.bot else '❌')
  embed.add_field(name='Booster', value=member.premium_since.strftime("%d-%b-%Y") if member.premium_since else '❌')
  embed.add_field(name='Activity', value=f'{str(member.activity.type).split(".")[-1].title()} **{str(member.activity.name)}**!' if member.activity else 'N/A')
  embed.add_field(name='Created at', value=member.created_at.strftime("%d-%b-%Y"))
  embed.add_field(name='Joined at', value=member.joined_at.strftime("%d-%b-%Y"))
  embed.set_thumbnail(url=member.display_avatar.url)
  embed.add_field(name='Roles', value="\n".join([x.mention for x in member.roles if x.name != '@everyone']) if len(member.roles) > 1 else 'N/A')
  embed.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
  await interaction.response.send_message(embed=embed, ephemeral=True)

# weather command
@bot.tree.command(description='Get the weather of a city. If no city is specified, the weather of Sousse will be displayed.')
async def weather(interaction: discord.Interaction, city : str = None):
  url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format("%20".join(city.split()), os.getenv('WEATHER_API_KEY')) if city else 'https://api.openweathermap.org/data/2.5/weather?q=Sousse&appid={}'.format(os.getenv('WEATHER_API_KEY'))

  response = requests.get(url)
  json_data = json.loads(response.text)
  
  if 'message' in json_data.keys():
    embed = discord.Embed(description=f':rolling_eyes: - {interaction.user.name} I can\'t find a city named **{city}**', color = 0xe74c3c)
    await interaction.response.send_message(embed=embed, ephemeral=True)
  else:
    country_code = json_data['sys']['country'].lower()
    city = json_data['name']
    weather_main = json_data['weather'][0]['main']
    weather_description = json_data['weather'][0]['description']
    weather_icon = 'https://openweathermap.org/img/wn/' + json_data['weather'][0]['icon'] + '@2x.png'
    temperature = str(round(json_data['main']['temp'] - 273.15, 2))
    feels_like = str(round(json_data['main']['feels_like'] - 273.15, 2))
    humidity = str(json_data['main']['humidity']) + '%'
    wind_speed = str(json_data['wind']['speed']) + 'm/s'

    embed = discord.Embed(title=f'Current weather in {city} :flag_{country_code}::', color=interaction.user.top_role.color)
    embed.add_field(name='Weather:', value=weather_main)
    embed.add_field(name='Description:', value=weather_description)
    embed.add_field(name='Temperature:', value=temperature)
    embed.add_field(name='Feels like:', value=feels_like)
    embed.add_field(name='Humidity:', value=humidity)
    embed.add_field(name='Wind speed:', value=wind_speed)
    embed.set_thumbnail(url=weather_icon)
    embed.set_footer(text=f'Requested by {interaction.user}', icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# meme command
@bot.tree.command(description='Returns a random meme from a subreddit.')
async def meme(interaction: discord.Interaction, subreddit : str = None):
  url = ' https://meme-api.com/gimme' if not subreddit else 'https://meme-api.com/gimme/{}'.format("".join(subreddit.lower()))

  response = requests.get(url)

  json_data = json.loads(response.text)
  if 'subreddit' in json_data.keys():
    subreddit = '/r/' + json_data['subreddit']
    if json_data['nsfw'] == True:
      await interaction.response.send_message('The meme you requested contains nsfw content.', ephemeral=True)
    else:
      await interaction.response.send_message(f'Here is a meme from {subreddit}\n{json_data["url"]}')
  else:
    embed = discord.Embed(description=f':rolling_eyes: - {interaction.user.name} I can\'t find a subreddit named **{subreddit}**', color = 0xe74c3c)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# fact command
@bot.tree.command(description='Returns a random fact.')
async def fact(interaction : discord.Interaction):
  embed = discord.Embed(title='Random Fact:', description=get_random_fact(), color=interaction.user.top_role.color)
  embed.set_thumbnail(url='https://image.shutterstock.com/image-illustration/fun-facts-colorful-stripes-260nw-683840437.jpg')
  embed.set_footer(text=f'Requested by {interaction.user}', icon_url=interaction.user.display_avatar.url)
  await interaction.response.send_message(embed=embed)

# snipe command
@bot.tree.command(name="snipe", description='Returns the last deleted message in the channel.')
@app_commands.checks.has_permissions(manage_messages=True)
async def snipe(interaction : discord.Interaction):
  deleted_messages_in_this_channel = [x for x in last_msg if x.channel.id == interaction.channel.id]
  if not deleted_messages_in_this_channel:
    embed = discord.Embed(description=f':no_entry: - There are no messages to snipe!', color=0xe74c3c)
    await interaction.response.send_message(embed=embed, ephemeral=True)
  else:
    embed = discord.Embed(title=f'There are {len(deleted_messages_in_this_channel)} messages deleted:', color=0xe74c3c)
    for msg in deleted_messages_in_this_channel:
        full_date = msg.created_at.strftime("%d-%b-%Y %X")
        splitted_date = full_date.split()
        joined_date = ' • '.join(splitted_date)
        embed.add_field(name=f'Message author is `{msg.author}` was sent in `#{msg.channel.name}`:', value=f':e_mail: - **{msg.content}**!\n{joined_date}', inline=False)
    embed.set_footer(text=f'Requested by {interaction.user}', icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@snipe.error
async def snipe_error(interaction : discord.Interaction, error : app_commands.AppCommandError):
  if isinstance(error, app_commands.MissingPermissions):
    embed = discord.Embed(title='Permission Error', description=':no_entry: - You are missing the required permissions to run this command!', color=0xe74c3c)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ping command
@bot.tree.command(description='Returns the bot\'s latency.')
async def ping(interaction: discord.Interaction):
  await interaction.response.send_message(f'✅ {round(bot.latency * 1000)}ms!', ephemeral=True)

# joke command
@bot.tree.command(description='Returns a random joke. You can also specify a word to search for in the joke.')
async def joke(interaction: discord.Interaction, contains : str = ''):
  url = 'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single&amount=1' if contains == '' else 'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single&contains={}&amount=1'.format(contains)
  response = requests.get(url)
  json_data = json.loads(response.text)
  if not json_data['error']:
    joke_category = json_data['category']
    joke = json_data['joke']
    embed = discord.Embed(title=f'{joke_category} Joke:', description=joke, color = interaction.user.top_role.color)
    embed.set_footer(text='Request by {}'.format(interaction.user),icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)
  else:
    embed = discord.Embed(description=':no_entry: - {} !'.format(json_data['causedBy'][0]), color=0xe74c3c)  
    await interaction.response.send_message(embed=embed, ephemeral=True)

#corona command
@bot.tree.command(description='Returns the corona stats of a country.')
async def corona(interaction: discord.Interaction, country : str = 'Tunisia'):
  url = "https://covid-193.p.rapidapi.com/statistics"
  country = country.title()
  if country == 'United States':
    country = "Usa"
  querystring = {"country":country}

  headers = {
	  "X-RapidAPI-Key": "ec2f8ccf8bmshbf1cf334816d19ep12966ejsnbf378abe0c43",
	  "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
  }

  response = requests.request("GET", url, headers=headers, params=querystring)

  json_data = json.loads(response.text)
  if json_data['results'] == 0:
    embed = discord.Embed(description=':rolling_eyes: - {} I can\'t find a country named **{}**!'.format(interaction.user.name, country), color=0xe74c3c)
    await interaction.response.send_message(embed=embed, ephemeral=True)
  else:
    url = "https://country-info.p.rapidapi.com/search"
    if country == 'Usa':
      country = 'United states'
    querystring = {"query":country}
    headers = {
      "X-RapidAPI-Key": "ec2f8ccf8bmshbf1cf334816d19ep12966ejsnbf378abe0c43",
      "X-RapidAPI-Host": "country-info.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    flag = json.loads(response.text)[0]['flag']
    embed = discord.Embed(title=f'Corona Statistics in {country} {flag}:', color=0xe74c3c)
    continent = json_data['response'][0]['continent']
    population = json_data['response'][0]['population']
    new_cases = json_data['response'][0]['cases']['new']
    active_cases = json_data['response'][0]['cases']['active']
    recovered_cases = json_data['response'][0]['cases']['recovered']
    total_cases = json_data['response'][0]['cases']['total']
    new_deaths = json_data['response'][0]['deaths']['new']
    total_deaths = json_data['response'][0]['deaths']['total']
    day = json_data['response'][0]['day']
    embed.add_field(name='Continent:', value=continent)
    embed.add_field(name='Country:', value=country)
    embed.add_field(name='Population:', value=population)
    embed.add_field(name='Total Cases:', value=total_cases)
    embed.add_field(name='Active Cases:', value=active_cases)
    embed.add_field(name='New Cases:', value=new_cases)
    embed.add_field(name='Recovered:', value=recovered_cases)
    embed.add_field(name='Total Deaths:', value=total_deaths)
    embed.add_field(name='New Deaths:', value=new_deaths)
    embed.set_author(name=day)
    embed.set_footer(text='Stay safe 🌸')
    await interaction.response.send_message(embed=embed)

# avatar command
@bot.tree.command(description='Returns the avatar of a member. You can also mention the member. Yours if none was mentioned.')
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
  if not member:
    member = interaction.user

  embed = discord.Embed(title="Avatar Link", url=member.display_avatar.url, color=member.top_role.color)
  embed.set_author(name=member, icon_url=member.display_avatar.url)
  embed.set_image(url=member.display_avatar.url)
  embed.set_footer(text='Requested by {}'.format(interaction.user), icon_url=interaction.user.display_avatar.url)
  await interaction.response.send_message(embed=embed, ephemeral=True)

# announce command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def announce(ctx: commands.Context, *, message: str = ''):
  corresponding_channels = {
    828940910053556224: 935969094652551189,
    783404400416391189: 783404401250795562,
  }
  await ctx.message.delete()
  channel = ctx.guild.get_channel(corresponding_channels[ctx.guild.id])
  if message or ctx.message.attachments:
    if message:
      await channel.send(message)

    if ctx.message.attachments:
      for img in ctx.message.attachments:
        await channel.send(file=await img.to_file())
  else:
    raise commands.CommandError
  
@announce.error
async def announce_error(ctx : commands.Context, error : commands.CommandError):
  if isinstance(error, commands.ChannelNotFound):
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(description=':rolling_eyes: - **{}**, I couldn\'t find a text channel named **{}**!'.format(ctx.author.name, ctx.message.content.split()[1]), color=0xe74c3c)
    await ctx.send(embed=embed)
  elif isinstance(error, commands.MissingRequiredArgument):
    embed = discord.Embed(title='Missing Arguments Error', description=':no_entry: - You are missing the required arguments to run this command!', color=0xe74c3c)
    embed.add_field(name='Command:', value='**&say `[Text Channel] [message]`**')
    await ctx.send(embed=embed)
  elif isinstance(error, commands.MissingPermissions):
    embed = discord.Embed(description=':no_entry: - **{}**, you don\'t have the required permissions to run this command!'.format(ctx.author.name), color=0xe74c3c)
    await ctx.send(embed=embed)
  elif isinstance(error, commands.CommandError):
    embed = discord.Embed(description=':no_entry: - **{}**, you didn\'t provide a message to send!'.format(ctx.author.name), color=0xe74c3c)
    await ctx.send(embed=embed)


# say command
@bot.tree.command(description='Sends a message in a channel. You can also mention the channel. Same channel if none was mentioned.')
@app_commands.checks.has_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, message: str, channel : discord.TextChannel = None):
  await interaction.response.defer(ephemeral=True)
  if message:
    if channel:
      await interaction.followup.send('Sent the message in {}!'.format(channel.mention), ephemeral=True)
      await channel.send(message)
    else:
      await interaction.followup.send('Sent the message in {}!'.format(interaction.channel.mention), ephemeral=True)
      await interaction.channel.send(message)
  else:
    raise app_commands.AppCommandError

@say.error
async def say_error(interaction: discord.Interaction, error: Exception):
  if isinstance(error, app_commands.AppCommandError):
    embed = discord.Embed(description=':rolling_eyes: - {} You didn\'t provide a message to send!'.format(interaction.user.name), color=0xe74c3c)
    await interaction.response.send_message(embed=embed, ephemeral=True)
  elif isinstance(error, app_commands.MissingPermissions):
    embed = discord.Embed(title='Permission Error', description=':no_entry: - You are missing the required permissions to run this command!', color=0xe74c3c)
    await interaction.response.send_message(embed=embed, ephemeral=True)
  else:
    embed = discord.Embed(title='Error', description=':no_entry: - An error occured while running this command!', color=0xe74c3c)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    print(error)


# icon command
@bot.tree.command(description='Returns the server\'s icon.')
async def icon(interaction: discord.Interaction):
  embed = discord.Embed(title="Icon Link",
  url=interaction.guild.icon.url,
  color=interaction.user.top_role.color)
  embed.set_author(name=interaction.guild.name,
  icon_url=interaction.guild.icon.url)
  embed.set_image(url=interaction.guild.icon.url)
  embed.set_footer(text='Requested by {}'.format(interaction.user),
  icon_url=interaction.user.display_avatar.url)
  await interaction.response.send_message(embed=embed, ephemeral=True)

# quote command
@bot.tree.command(description='Returns a random quote.')
async def quote(interaction: discord.Interaction):
  quote = get_random_quote().split('|')[0]
  author = get_random_quote().split('|')[1]
  embed = discord.Embed(title='Quote:',
  description=quote,
  color=interaction.user.top_role.color)
  embed.add_field(name='Author:', value=f':book: *{author}*')
  embed.set_footer(text='Requested by {}'.format(interaction.user), icon_url=interaction.user.display_avatar.url)
  await interaction.response.send_message(embed=embed)

# -------------------------------------------- Run Bot -------------------------------------------- #

bot.run(os.getenv('TOKEN'))
