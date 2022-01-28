import discord
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from discord.ext import commands
from discord.ext import tasks
from PIL import Image, ImageFont, ImageDraw
import os
import requests
import json
#from keep_alive import keep_alive
import logging
import asyncio

intents = discord.Intents(members=True, guilds=True, bans=True, invites=True, messages=True, guild_messages=True, dm_reactions=True, emojis=True, dm_messages=True, reactions=True, presences=True)
logging.basicConfig(level=logging.INFO)
activity = discord.Activity(type=discord.ActivityType.listening, name="&help")
bot = commands.Bot(command_prefix='&', intents=intents, activity=activity)
bot.remove_command('help')
cmds = [
  {
    'name' : 'avatar',  
    'args' : '[member]',
    'dis' : 'Returns the avatar of the member mentioned or the user who called the command (in case no one was mentioned).'
  },
  {
    'name' : 'meme',  
    'args' : '[subreddit name]',
    'dis' : 'Returns a random meme from the subbredit you provided or Dankmemes/memes/me_irl (in case no Subbredit name was provided).'
  },
  { 
    'name' : 'weather',  
    'args' : '[city name]',
    'dis' : 'Returns current weather in the city mentioned or Sousse if no city was mentioned.'
  },
  {
    'name' : 'say',
    'args' : '[message]',
    'dis' : 'Sends the message as the bot.'
  },
  {
    "name" : 'fact', 
    'args' : '',
    'dis' : 'Returns a random fact.'
  },
  {
    "name" : 'corona', 
    'args' : '[country name]',
    'dis' : 'Returns today''s COVID-19 statistics of the mentioned country (Tunisia if none was mentioned).'
  },
  {
    "name" : 'snipe',  
    'args' : '',
    'dis' : 'Returns last deleted messages in the channel where the command was called.'
  },
  {
    "name" : 'rps', 
    'args' : '[member]',
    'dis' : 'Creates a RPS game between you and the mentioned member.'
  },
  {
    "name" : 'joke', 
    'args' : '[word]',
    'dis' : 'Returns a random joke contains the word (word argument can be omitted).'
  },
  {
    "name" : 'movie', 
    'args' : '[movie/serie name]',
    'dis' : 'Returns detailed information about the movie/serie mentioned.'
  },
  {
    "name" : 'ping', 
    'args' : '',
    'dis' : 'Returns current bot\'s ping.'
  },
  {
    "name" : 'quote', 
    'args' : '',
    'dis' : 'Returns a random quote.'
  },
  {
    "name" : 'userinfo', 
    'args' : '[member]',
    'dis' : 'Shows detailed information about the mentioned member or the user in case no one was mentioned.'
  },
  {
    "name" : 'serverinfo', 
    'args' : '',
    'dis' : 'Shows detailed information about the server where the command was called.'
  },
  {
    "name" : 'help', 
    'args' : '[command]',
    'dis' : 'Shows this message if no command was provided.'
  }
]

@tasks.loop(minutes=3)
async def member_count():
  for guild in bot.guilds:
    overwrites = {
      guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False)
    }
    found = False
    for vc in guild.voice_channels:
      if vc.name.startswith('Member count:'):
        await vc.edit(name='Member count: {}'.format(guild.member_count), overwrites=overwrites, user_limit=0, position=0)
        found = True
        break
    if not found:
      await guild.create_voice_channel(name='Member count: {}'.format(guild.member_count), overwrites=overwrites, position=0, user_limit=0)
  print('Updated')  
member_count.start()

@bot.event
async def on_ready():
  DiscordComponents(bot)
  print('------')
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print('------')
  for guild in bot.guilds:
    if not guild.id in [828940910053556224, 783404400416391189]:
      await guild.owner.send(':rolling_eyes: Sorry, i left `{}` because i\'m a private bot that only works in `GDSC ISSATSo Community Server!`'.format(guild.name))
      await guild.leave()


@bot.event
async def on_member_join(member):
  if member.guild.id == 828940910053556224:
    welcome_channel = bot.get_channel(935969094652551189)
    current_counter = member.guild.member_count
  else:
    current_counter = member.guild.member_count
    welcome_channel = bot.get_channel(783406528165838888)
    rules_channel = bot.get_channel(841102973206659134)
    await rules_channel.send(member.mention, delete_after=0.1)
  if not member.bot:

    avatar_file_name = "avatar.png"
    await member.avatar_url.save(avatar_file_name)
    avatar = Image.open("avatar.png")
    avatar = avatar.resize((256, 256))

    mask_im = Image.new("L", avatar.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0, 0, 256, 256), fill=255, outline=126, width=10)
    mask_im.save('mask_circle.png', quality=95)

    background = Image.open('GDSC Welcome Template.png')
    font = ImageFont.truetype("OpenSans.ttf", 40)
    background_copy = background.copy()
    background_copy.paste(avatar, (230, 20), mask_im)
    draw = ImageDraw.Draw(background_copy)
    draw.text((150, 280), 'WELCOME', (144, 240, 116), font=font)
    draw.text((360, 280), '{}'.format(member.display_name), (227, 139, 11), font=font)
    draw.text((15, 320), 'To', (60, 126, 250), font=font)
    draw.text((70, 320), 'GDSC ISSATSo', (250, 46, 24), font=font)
    draw.text((340, 320), 'Community Server!', (60, 126, 250), font=font)
    
    background_copy.save("member_joined.png")

    await welcome_channel.send(content=f'Welcome {member.mention} to **GDSC ISSATSo Community Server**. **Enjoy** your stay!', file=discord.File("member_joined.png"))
    await asyncio.sleep(1)
    os.remove("member_joined.png")
    os.remove("avatar.png")
    os.remove('mask_circle.png')

@bot.event
async def on_guild_join(guild):
  if not guild.id in [828940910053556224, 783404400416391189]:
    await guild.owner.send(':rolling_eyes: Sorry, i left `{}` because i\'m a private bot that only works in `GDSC ISSATSo Community Server!`'.format(guild.name))
    await guild.leave()

def get_random_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  random_quote = f'{json_data[0]["q"]}|{json_data[0]["a"]}'
  return random_quote


def get_random_fact():
  response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
  json_data = json.loads(response.text)
  useless_fact = f'{json_data["text"]}'
  return useless_fact


#help command
@bot.group(invoke_without_command=True)
async def help(ctx):
  embed1 = discord.Embed(title='Commands:', color=0x70e68a)
  embed2 = discord.Embed(title='Commands:', color=0x70e68a)
  embed3 = discord.Embed(title='Commands:', color=0x70e68a)
  embed1.set_footer(text='Requested by {}'.format(ctx.author), icon_url = ctx.author.avatar_url)
  embed1.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
  embed2.set_footer(text='Requested by {}'.format(ctx.author), icon_url = ctx.author.avatar_url)
  embed2.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
  embed3.set_footer(text='Requested by {}'.format(ctx.author), icon_url = ctx.author.avatar_url)
  embed3.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
  global cmds
  counter = 0
  for cmd in cmds:
    counter += 1
    if counter <= 5:
      embed1.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`&{cmd["name"]} {cmd["args"]}` : {cmd["dis"]}', inline=False)
    elif counter > 5 and counter <= 10:
      embed2.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`&{cmd["name"]} {cmd["args"]}` : {cmd["dis"]}', inline=False)
    else:
      embed3.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`&{cmd["name"]} {cmd["args"]}` : {cmd["dis"]}', inline=False)

  listOfEmbeds = [embed1, embed2, embed3] 
  currentPage = 0 
  message = await ctx.reply(
        embed = listOfEmbeds[currentPage],
        mention_author=False,
        components = [
            [
                Button(
                    label = "Prev",
                    style = ButtonStyle.green
                ),
                Button(
                    label = f"Page {int(listOfEmbeds.index(listOfEmbeds[currentPage])) + 1}/{len(listOfEmbeds)}",
                    style = ButtonStyle.grey,
                    disabled = True
                ),
                Button(
                    label = "Next",
                    style = ButtonStyle.green
                )
            ]
        ]
    )
  while True:
      try:
        interaction = await bot.wait_for(
            "button_click",
            check = lambda i: i.component.label in ["Prev", "Next"],
            timeout = 15.0
        )
        if interaction.component.label == "Prev" and interaction.user.id == ctx.author.id:
            currentPage -= 1
        elif interaction.component.label == "Next" and interaction.user.id == ctx.author.id:
            currentPage += 1
        if currentPage == len(listOfEmbeds):
            currentPage = 0
        elif currentPage < 0:
            currentPage = len(listOfEmbeds) - 1
  
        if interaction.component.label in ["Prev", "Next"] and interaction.user.id == ctx.author.id:
          await interaction.respond(
          type = InteractionType.UpdateMessage,
          embed = listOfEmbeds[currentPage],
          components = [
              [
                  Button(
                      label = "Prev",
                      style = ButtonStyle.green
                  ),
                  Button(
                      label = f"Page {int(listOfEmbeds.index(listOfEmbeds[currentPage])) + 1}/{len(listOfEmbeds)}",
                      style = ButtonStyle.grey,
                      disabled = True
                  ),
                  Button(
                      label = "Next",
                      style = ButtonStyle.green
                  )
              ]
          ]
        )
        else:
          await interaction.respond(
            type = InteractionType.ChannelMessageWithSource,
            content = 'This is not your help command!',
        )          
      except asyncio.TimeoutError:
        await message.edit(
            components = [
                [
                    Button(
                        label = "Prev",
                        style = ButtonStyle.green,
                        disabled = True
                    ),
                    Button(
                        label = f"Page {int(listOfEmbeds.index(listOfEmbeds[currentPage])) + 1}/{len(listOfEmbeds)}",
                        style = ButtonStyle.grey,
                        disabled = True
                    ),
                    Button(
                        label = "Next",
                        style = ButtonStyle.green,
                        disabled = True
                    )
                ]
            ]
        )
        break
  

def generate_embed(title, description, author, fields : dict, color = 0x70e68a) -> discord.Embed:
  embed = discord.Embed(title=title, description=description, color = color)
  embed.add_field(name='Usage:', value="\n".join(fields['usage']))
  embed.add_field(name='Examples:', value="\n".join(fields['examples']))
  embed.set_footer(text='Requested by {}'.format(author), icon_url=author.avatar_url)

  return embed

  
@help.command()
async def avatar(ctx):
  embed = generate_embed('Avatar', 'Returns the avatar of the member mentioned or the user who called the command (in case no one was mentioned).', ctx.author, {'usage' : ['&avatar', '&avatar server', '&avatar [user]'], 'examples' : ['&avatar', '&avatar server', '&avatar {}'.format(ctx.author.mention)]})
  await ctx.send(embed=embed)


@help.command()
async def meme(ctx):
  embed = generate_embed('Meme', 'Returns a random meme from the subbredit you provided or Dankmemes/memes/me_irl (in case no Subbredit name was provided).', ctx.author, {'usage' : ['&meme', '&meme [subreddit name]'], 'examples' : ['&meme', '&meme me_irl']})
  await ctx.send(embed=embed)


@help.command()
async def weather(ctx):
  embed = generate_embed('Weather', 'Returns current weather in the city mentioned or Sousse if no city was mentioned.', ctx.author, {'usage' : ['&weather', '&weather [city name]'], 'examples' : ['&weather', '&weather Monastir']})
  await ctx.send(embed=embed)


@help.command()
async def say(ctx):
  embed = generate_embed('Say', 'Sends the message that the user provided as the bot.', ctx.author, {'usage' : ['&say [message]'], 'examples' : ['&say Hello World!']})
  await ctx.send(embed=embed)


@help.command()
async def fact(ctx):
  embed = generate_embed('Fact', 'Return a random fact', ctx.author, {'usage' : ['&fact'], 'examples' : ['&fact']})
  await ctx.send(embed=embed)


@help.command()
async def corona(ctx):
  embed = generate_embed('Corona', 'Returns today''s COVID-19 statistics of the mentioned country (Tunisia if none was mentioned).', ctx.author, {'usage' : ['&corona', '&corona [country name]'], 'examples' : ['&corona', '&corona Morocco']})
  await ctx.send(embed=embed)


@help.command()
async def snipe(ctx):
  embed = generate_embed('Snipe (Certain Permission are Required)', 'Returns last deleted messages in the channel where the command was called.', ctx.author, {'usage' : ['&snipe'], 'examples' : ['&snipe']})
  await ctx.send(embed=embed)


@help.command()
async def rps(ctx):
  embed = generate_embed('RPS', 'Creates a RPS game between you and the mentioned member.', ctx.author, {'usage' : ['&rps [member]'], 'examples' : ['&rps {0.mention}'.format(ctx.author), '&rps 195605500488384512']})
  await ctx.send(embed=embed)

@help.command()
async def joke(ctx):
  embed = generate_embed('Joke', 'Returns a random joke contains the word (word argument can be omitted).', ctx.author, {'usage' : ['&joke', '&joke [word]'], 'examples' : ['&joke', '&joke christmas']})
  await ctx.send(embed=embed)

@help.command()
async def movie(ctx):
  embed = generate_embed('Movie', 'Returns detailed information about the movie/serie mentioned.', ctx.author, {'usage' : ['&movie [movie/serie name]'], 'examples' : ['&movie Red Notice', '&movie Breaking Bad']})
  await ctx.send(embed=embed)

@help.command()
async def ping(ctx):
  embed = generate_embed('Ping', 'Returns Bot\'s current client ping.', ctx.author, {'usage' : ['&ping'], 'examples' : ['&ping']})
  await ctx.send(embed=embed)

@help.command()
async def quote(ctx):
  embed = generate_embed('Quote', 'Returns a random quote.', ctx.author, {'usage' : ['&quote'], 'examples' : ['&quote']})
  await ctx.send(embed=embed)


@help.command()
async def userinfo(ctx):
  embed = generate_embed('User Info', 'Shows detailed information about the mentioned member or the user in case no one was mentioned.', ctx.author, {'usage' : ['&userinfo', '&userinfo [member]'], 'examples' : ['&userinfo', '&userinfo {0.mention}'.format(ctx.author), '&userinfo 195605500488384512']})
  await ctx.send(embed=embed)



@help.command()
async def serverinfo(ctx):
  embed = generate_embed('Server Info', 'Shows detailed information about the server where the command was called.', ctx.author, {'usage' : ['&serverinfo'], 'examples' : ['&serverinfo']})
  await ctx.send(embed=embed)

@help.command()
async def help(ctx):
  embed = generate_embed('Help', 'Shows this message if no command was provided.', ctx.author, {'usage' : ['&help', '&help [command]'], 'examples' : ['&help', '&help avatar']})
  await ctx.send(embed=embed)


#Server Info Command
@bot.command(name='serverinfo')
async def server_info(ctx):
  guild_name =ctx.guild.name
  guild_text_channels = len(ctx.guild.text_channels)
  guild_voice_channels = len(ctx.guild.voice_channels)
  guild_categories = len(ctx.guild.categories)
  guild_member_count = ctx.guild.member_count
  guild_human_members = len([x for x in ctx.guild.members if not x.bot])
  guild_bot_members = guild_member_count - guild_human_members
  guild_banned_members = len(await ctx.guild.bans())
  guild_member_statuses = f'🟢 {len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members)))} 🟠 {len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members)))} 🔴 {len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members)))} ⚪ {len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))}'
  guild_roles_count = len(ctx.guild.roles)
  guild_highest_role = ctx.guild.roles[-1].mention
  guild_description = ctx.guild.description if ctx.guild.description else 'N/A'
  footer_text ='Guild ID: {} • Created at: {}'.format(ctx.guild.id, ctx.guild.created_at.strftime("%d-%b-%Y"))
  embed = discord.Embed(title='Server information', color=ctx.author.top_role.color)
  embed.add_field(name='Name:', value=guild_name)
  embed.add_field(name='Avatar:', value="[Click Here]({})".format(ctx.guild.icon_url))
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
  embed.add_field(name='Invites:', value=len(await ctx.guild.invites()))
  embed.add_field(name='Description:', value=guild_description, inline=False)
  embed.set_thumbnail(url=ctx.guild.icon_url)
  embed.set_footer(text=footer_text)
  await ctx.reply(embed=embed, mention_author=False)


#User info command
@bot.command(name='userinfo')
async def user_info(ctx, *, member : discord.Member = None):
  statuses = {
    'online' : '🟢 Online',
    'idle' : '🟠 Idle',
    'dnd' : '🔴 Do not Disturb',
    'offline' : '⚪ Offline'
  }
  if not member:
    member = ctx.author
  embed = discord.Embed(title='User information:', color = member.top_role.color)
  embed.add_field(name='Name', value=member)
  embed.add_field(name='ID', value=member.id)
  embed.add_field(name='Roles', value="\n".join([x.mention for x in member.roles if x.name != '@everyone']) if len(member.roles) > 1 else 'N/A')
  embed.add_field(name='Bot?', value='✅' if member.bot else '❌')
  embed.add_field(name='Booster', value=member.premium_since.strftime("%d-%b-%Y") if member.premium_since else '❌')
  embed.add_field(name='Status', value=statuses[str(member.status)])
  embed.add_field(name='Activity', value=f'{str(member.activity.type).split(".")[-1].title()} **{str(member.activity.name)}**!' if member.activity else 'N/A')
  embed.add_field(name='Created at', value=member.created_at.strftime("%d-%b-%Y"))
  embed.add_field(name='Joined at', value=member.joined_at.strftime("%d-%b-%Y"))
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text='Requested by {}'.format(ctx.author), icon_url = ctx.author.avatar_url)
  await ctx.reply(embed=embed, mention_author=False)

@user_info.error
async def user_info_error(ctx, error : commands.CommandError):
  if isinstance(error, commands.MemberNotFound):
    embed = discord.Embed(description=f':rolling_eyes: - {ctx.author.name}, I can\'t find **{" ".join(ctx.message.content.split()[1:])}**!', color=0xe74c3c)
    await ctx.message.add_reaction('❌')
    await ctx.send(embed=embed)
    print(error)

#weather command
@bot.command()
async def weather(ctx, *, city : str = None):
  url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format("%20".join(city.split()), os.getenv('WEATHER')) if city else 'https://api.openweathermap.org/data/2.5/weather?q=Sousse&appid={}'.format(os.getenv('WEATHER'))

  response = requests.get(url)
  json_data = json.loads(response.text)
  
  if 'message' in json_data.keys():
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(description=f':rolling_eyes: - {ctx.author.name} I can\'t find a city named **{city}**', color = 0xe74c3c)
    await ctx.reply(embed=embed, mention_author=False)
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

    embed = discord.Embed(title=f'Current weather in {city} :flag_{country_code}::', color=ctx.author.top_role.color)
    embed.add_field(name='Weather:', value=weather_main)
    embed.add_field(name='Description:', value=weather_description)
    embed.add_field(name='Temperature:', value=temperature)
    embed.add_field(name='Feels like:', value=feels_like)
    embed.add_field(name='Humidity:', value=humidity)
    embed.add_field(name='Wind speed:', value=wind_speed)
    embed.set_thumbnail(url=weather_icon)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=embed, mention_author=False)

#meme command
@bot.command()
async def meme(ctx, *, subreddit : str = None):
  url = ' https://meme-api.herokuapp.com/gimme' if not subreddit else ' https://meme-api.herokuapp.com/gimme/{}'.format("".join(subreddit.lower()))

  response = requests.get(url)

  json_data = json.loads(response.text)
  if 'subreddit' in json_data.keys():
    subreddit = '/r/' + json_data['subreddit']
    if json_data['nsfw'] == True:
      await ctx.reply('The meme you requested contains nsfw content.', delete_after=5, mention_author=False)
      await asyncio.sleep(5)
      await ctx.message.delete()
    else:
      await ctx.reply('Here is a meme from {}'.format(subreddit), mention_author=False)
      await ctx.send(json_data['url'])
  else:
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(description=f':rolling_eyes: - {ctx.author.name} I can\'t find a subreddit named **{subreddit}**', color = 0xe74c3c)
    await ctx.reply(embed=embed, mention_author=False)

#fact command
@bot.command()
async def fact(ctx):
  embed = discord.Embed(title='Random Fact:', description=get_random_fact(), color=ctx.author.top_role.color)
  embed.set_thumbnail(url='https://image.shutterstock.com/image-illustration/fun-facts-colorful-stripes-260nw-683840437.jpg')
  embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
  await ctx.reply(embed=embed, mention_author=False)

#rps command
@bot.command()
async def rps(ctx, *, member : discord.Member):
  if ctx.author == member or member.bot:
    raise commands.MemberNotFound
  else:
    message = await ctx.send('`Creating a RPS game...`', mention_author=False)
    embed = discord.Embed(title='Rock Paper Scissors:', description='**Who will win? 🤔**', color=ctx.author.top_role.color)
    embed.set_thumbnail(url='https://facts.net/wp-content/uploads/2020/11/rock-paper-scissors.jpg')
    embed.add_field(name='Player 1:', value=ctx.author.name)
    embed.add_field(name='Player 2:', value=member.name)
    await ctx.send(embed=embed)
    embed.description = '**Choose an option from below:**'
    player1_msg = await ctx.author.send(
      embed=embed,
      components = [
        [
          Button(
            label = "🪨 Rock",
            style = ButtonStyle.grey
          ),
          Button(
            label = "🧻 Paper",
            style = ButtonStyle.blue
          ),
          Button(
            label = "✂️ Scissors",
            style = ButtonStyle.red
          )
        ]
      ])
    await message.edit(content='`Game created successfully` *(Check DMs)*')
    try:
      interaction1 = await bot.wait_for(
        "button_click",
        check=lambda i: i.component.label in ['🪨 Rock', '🧻 Paper', '✂️ Scissors'] and i.user.id == ctx.author.id,
        timeout=30
      )

      await interaction1.respond(
        type = InteractionType.UpdateMessage,
        embed = embed,
        components = [
          [
            Button(
              label = "🪨 Rock",
              style = ButtonStyle.grey,
              disabled = True
            ),
            Button(
              label = "🧻 Paper",
              style = ButtonStyle.blue,
              disabled = True
            ),
            Button(
              label = "✂️ Scissors",
              style = ButtonStyle.red,
              disabled = True
            )
          ]
        ]
      )
      player1_choice = await ctx.author.send('You chose **`{}`**, Please wait for the other oponent to choose...'.format(interaction1.component.label))
      player2_msg = await member.send(
        embed=embed,
        components = [
          [
            Button(
              label = "🪨 Rock",
              style = ButtonStyle.grey
            ),
            Button(
              label = "🧻 Paper",
              style = ButtonStyle.blue
            ),
            Button(
              label = "✂️ Scissors",
              style = ButtonStyle.red
            )
          ]
        ])

      interaction2 = await bot.wait_for(
        'button_click',
        check=lambda i: i.component.label in ['🪨 Rock', '🧻 Paper', '✂️ Scissors'] and i.user.id == member.id,
        timeout=30
      )

      await interaction2.respond(
        type = InteractionType.UpdateMessage,
        embed = embed,
        components = [
          [
            Button(
              label = "🪨 Rock",
              style = ButtonStyle.grey,
              disabled = True
            ),
            Button(
              label = "🧻 Paper",
              style = ButtonStyle.blue,
              disabled = True
            ),
            Button(
              label = "✂️ Scissors",
              style = ButtonStyle.red,
              disabled = True
            )
          ]
        ]
      )
      await player1_choice.delete()
      arr = ['Rock&Scissors', 'Paper&Rock', 'Scissors&Paper']
      choice1 = "".join([c for c in interaction1.component.label if c.isalpha()])
      choice2 = "".join([c for c in interaction2.component.label if c.isalpha()])
      print(choice1, choice2)
      print("&".join([choice1, choice2]))
      print("&".join([choice1, choice2]) in arr)
      if interaction1.component.label == interaction2.component.label:
        embed = discord.Embed(title='Results', color=ctx.author.top_role.color)
        embed.add_field(name=f'{interaction1.component.label[0]} == {interaction2.component.label[0]}', value='**It\'s a Tie!**', inline=False)
        embed.set_author(name='Game Over!')
        embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6R63nEBSwQBGBICTHQrcbC9SAd_tdLR9k3w&usqp=CAU')
        embed.set_footer(text='Game made by Younes#5003', icon_url='https://cdn.discordapp.com/avatars/387798722827780108/7b2a3c20de224aa0b0c49856927d2d4a.webp?size=1024')
        await message.delete()
        await ctx.send(embed=embed)
        await ctx.author.send(embed=embed)
        await member.send(embed=embed)
      elif ("&".join([choice1, choice2]) in arr):
        embed = discord.Embed(title='Results', color=ctx.author.top_role.color)
        embed.add_field(name=f'{interaction1.component.label[0]} > {interaction2.component.label[0]}', value=f'🥳 **{ctx.author.name}** Won! 🥳')
        embed.set_author(name='Game Over!')
        embed.set_thumbnail(url='https://www.pinclipart.com/picdir/big/576-5762132_player-1-wins-clipart.png')
        embed.set_footer(text='Game made by Younes#5003', icon_url='https://cdn.discordapp.com/avatars/387798722827780108/7b2a3c20de224aa0b0c49856927d2d4a.webp?size=1024')
        await message.delete()
        await ctx.send(embed=embed)
        await ctx.author.send(embed=embed)
        await member.send(embed=embed)
      else:
        embed = discord.Embed(title='Results', color=ctx.author.top_role.color)
        embed.add_field(name=f'{interaction2.component.label[0]} > {interaction1.component.label[0]}', value=f'🥳 **{member.name}** Won! 🥳')
        embed.set_author(name='Game Over!')
        embed.set_thumbnail(url='http://learnlearn.uk/scratch/wp-content/uploads/sites/7/2018/01/player2png.png')
        embed.set_footer(text='Game made by Younes#5003', icon_url='https://cdn.discordapp.com/avatars/387798722827780108/7b2a3c20de224aa0b0c49856927d2d4a.webp?size=1024')
        await message.delete()
        await ctx.send(embed=embed)
        await ctx.author.send(embed=embed)
        await member.send(embed=embed)
      await player1_msg.edit(
        components = [
          [
            Button(
              label = "🪨 Rock",
              style = ButtonStyle.grey,
              disabled = True
            ),
            Button(
              label = "🧻 Paper",
              style = ButtonStyle.blue,
              disabled = True
            ),
            Button(
              label = "✂️ Scissors",
              style = ButtonStyle.red,
              disabled = True
            )
          ]
        ]
      )
      await player2_msg.edit(
        components = [
          [
            Button(
              label = "🪨 Rock",
              style = ButtonStyle.grey,
              disabled = True
            ),
            Button(
              label = "🧻 Paper",
              style = ButtonStyle.blue,
              disabled = True
            ),
            Button(
              label = "✂️ Scissors",
              style = ButtonStyle.red,
              disabled = True
            )
          ]
        ]
      )
    except asyncio.TimeoutError:
      await message.delete()
      await ctx.send(f"{ctx.author.mention}, {member.mention}: `Game cancelled, timed out.`")
      await player1_msg.edit(
        components = [
          [
            Button(
              label = "🪨 Rock",
              style = ButtonStyle.grey,
              disabled = True
            ),
            Button(
              label = "🧻 Paper",
              style = ButtonStyle.blue,
              disabled = True
            ),
            Button(
              label = "✂️ Scissors",
              style = ButtonStyle.red,
              disabled = True
            )
          ]
        ]
      )
      await player2_msg.edit(
        components = [
          [
            Button(
              label = "🪨 Rock",
              style = ButtonStyle.grey,
              disabled = True
            ),
            Button(
              label = "🧻 Paper",
              style = ButtonStyle.blue,
              disabled = True
            ),
            Button(
              label = "✂️ Scissors",
              style = ButtonStyle.red,
              disabled = True
            )
          ]
        ]
      )
      return

@rps.error
async def rps_error(ctx, error : commands.CommandError):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(title='Missing Arguments Error', description=':no_entry: - You are missing the required arguments to run this command!', color=0xe74c3c)
    embed.add_field(name='Command:', value='**&rps `[member]`**')
    await ctx.send(embed=embed)
  elif isinstance(error, commands.MemberNotFound):
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(title='Member Not Found Error', description=':no_entry: - Invalid opponent please mention another player!', color=0xe74c3c)
    await ctx.send(embed=embed)
  else:
    print(error)

#movie command
@bot.command()
@commands.guild_only()
async def movie(ctx, *, search_term : str):
  response = requests.get("https://imdb-api.com/en/API/SearchAll/k_g8yoa1tc/{}".format("%20".join(search_term.lower().split())))
  json_data = json.loads(response.text)
  if not json_data['results'] or json_data['results'][0]['resultType'] != 'Title':
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(description=':rolling_eyes: - No movies/series were found that match your provided filter(s).!', color=0xe74c3c)
    await ctx.reply(embed=embed, mention_author=False)
  else:
    movie_id = json_data['results'][0]['id']
    url = "https://imdb-api1.p.rapidapi.com/Title/k_g8yoa1tc/{}".format(movie_id)

    headers = {
        'x-rapidapi-host': "imdb-api1.p.rapidapi.com",
        'x-rapidapi-key': "ec2f8ccf8bmshbf1cf334816d19ep12966ejsnbf378abe0c43"
        }

    response = requests.request("GET", url, headers=headers)

    json_data = json.loads(response.text)
    title = json_data['title']
    type = json_data['type']
    year = json_data['year']
    image_url = json_data['image']
    release_date = json_data['releaseDate']
    length = json_data['runtimeStr'] if type == 'Movie' else '{} Seasons'.format(len(json_data['tvSeriesInfo']['seasons']))
    summary = json_data['plot']
    awards = json_data['awards'] if json_data['awards'] else 'N/A'
    directors = json_data['directors'] if json_data['directors'] else 'N/A'
    writers = json_data['writers'] if json_data['writers'] else json_data['tvSeriesInfo']['creators']
    stars = json_data['stars']
    genres = json_data['genres']
    countries = json_data['countries']
    languages = json_data['languages']
    rating = json_data['imDbRating']
    budget = json_data['boxOffice']['budget'].split()[0] if json_data['boxOffice']['budget'] else 'N/A'

    embed = discord.Embed(title=f'{title} ({year}) ({type})', color=ctx.author.top_role.color)
    embed.add_field(name='Stars:', value=stars, inline=False)
    embed.add_field(name='Awards:', value=awards)
    embed.add_field(name='Budget:', value=budget)
    embed.add_field(name='Countries:', value=countries)
    embed.add_field(name='Directors:', value=directors)
    embed.add_field(name='Release Date:', value=release_date)
    embed.add_field(name='Length:', value=length)
    embed.add_field(name='Genres:', value=genres)
    embed.add_field(name='Languages:', value=languages)
    embed.add_field(name='IMDB Rating:', value=rating)
    embed.add_field(name='Summary:', value=summary)
    embed.set_thumbnail(url=image_url)
    embed.set_footer(text=f'Writers: {writers}', icon_url=image_url)

    await ctx.reply(embed=embed, mention_author=False)


@movie.error
async def movie_error(ctx : commands.Context, error : commands.CommandError):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(title='Missing Arguments Error', description=':no_entry: - You are missing the required arguments to run this command!', color=0xe74c3c)
    embed.add_field(name='Command:', value='**&movie `[movie/serie name]`**')
    await ctx.send(embed=embed)


last_msg = []
@bot.event
async def on_message_delete(message):
  global last_msg
  if not message.author.bot:
    last_msg.append(message)
  await asyncio.sleep(60)
  if len(last_msg) > 10:
    last_msg.clear()

#snipe command
@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_messages=True)
async def snipe(ctx : commands.Context):
  deleted_messages_in_this_channel = [x for x in last_msg if x.channel.id == ctx.message.channel.id]
  if not deleted_messages_in_this_channel:
    embed = discord.Embed(description=f':no_entry: - There are no messages to snipe!', color=0xe74c3c)
    await ctx.message.add_reaction('❌')
    await ctx.reply(embed=embed, mention_author=False)
  else:
    embed = discord.Embed(title=f'There are {len(deleted_messages_in_this_channel)} messages deleted:', color=0xe74c3c)
    for msg in deleted_messages_in_this_channel:
        full_date = msg.created_at.strftime("%d-%b-%Y %X")
        splitted_date = full_date.split()
        joined_date = ' • '.join(splitted_date)
        embed.add_field(name=f'Message author is {msg.author} was sent in `{msg.channel.name}`:', value=f':e_mail: - **{msg.content}**!\n{joined_date}', inline=False)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=embed, mention_author=False)

@snipe.error
async def snipe_error(ctx : commands.Context, error : commands.CommandError):
  if isinstance(error, commands.MissingPermissions):
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(title='Permission Error', description=':no_entry: - You are missing the required permissions to run this command!', color=0xe74c3c)
    await ctx.send(embed=embed)

#ping command
@bot.command()
@commands.guild_only()
async def ping(ctx):
  await ctx.reply(f'✅ {round(bot.latency * 1000)}ms!', mention_author=False)

#joke command
@bot.command()
@commands.guild_only()
async def joke(ctx, *, contains : str = ''):
  url = 'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single&amount=1' if contains == '' else 'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single&contains={}&amount=1'.format(contains)
  response = requests.get(url)
  json_data = json.loads(response.text)
  if json_data['error'] != True:
    joke_category = json_data['category']
    joke = json_data['joke']
    embed = discord.Embed(title=f'{joke_category} Joke:', description=joke, color = ctx.author.top_role.color)
    embed.set_footer(text='Request by {}'.format(ctx.author),icon_url=ctx.author.avatar_url)
  else:
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(description=':no_entry: - {} !'.format(json_data['causedBy'][0]), color=0xe74c3c)  
  await ctx.reply(embed=embed, mention_author=False)


#corona command
@bot.command()
@commands.guild_only()
async def corona(ctx, *, country : str = ''):
  url = "https://covid-193.p.rapidapi.com/statistics"
  country = 'Tunisia' if country == '' else country
  querystring = {"country":country}

  headers = {
      'x-rapidapi-host': "covid-193.p.rapidapi.com",
      'x-rapidapi-key': "ec2f8ccf8bmshbf1cf334816d19ep12966ejsnbf378abe0c43"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)

  json_data = json.loads(response.text)
  if json_data['results'] == 0:
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(description=':rolling_eyes: - {} I can\'t find a country named **{}**!'.format(ctx.author.name, country), color=0xe74c3c)
    await ctx.reply(embed=embed, mention_author=False)
  else:
    country = json_data['response'][0]['country']
    url = "https://covid-19-data.p.rapidapi.com/country"

    querystring = {"name":country,"format":"json"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "ec2f8ccf8bmshbf1cf334816d19ep12966ejsnbf378abe0c43"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    country_code = json.loads(response.text)[0]['code'].lower()
    continent = json_data['response'][0]['continent']
    population = json_data['response'][0]['population']
    new_cases = json_data['response'][0]['cases']['new']
    active_cases = json_data['response'][0]['cases']['active']
    recovered_cases = json_data['response'][0]['cases']['recovered']
    total_cases = json_data['response'][0]['cases']['total']
    new_deaths = json_data['response'][0]['deaths']['new']
    total_deaths = json_data['response'][0]['deaths']['total']
    day = json_data['response'][0]['day']
    embed = discord.Embed(title=f'Corona Statistics in {country} :flag_{country_code}::',
    color=0xe74c3c)
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
    await ctx.reply(embed=embed, mention_author=False)

#avatar command
@bot.command()
@commands.guild_only()
async def avatar(ctx, *, member : str = ''):
  if len(member) > 0:
    if '!' in member:
      member = ctx.guild.get_member(int(member[3:-1]))
      embed = discord.Embed(title="Avatar Link",
      url=member.avatar_url,
      color=member.top_role.color)
      embed.set_author(name=member,
      icon_url=member.avatar_url)
      embed.set_image(url=member.avatar_url_as(format='gif') if member.is_avatar_animated() else member.avatar_url_as(format='png'))
      embed.set_footer(text='Requested by {}'.format(ctx.author),
      icon_url=ctx.author.avatar_url)
      await ctx.reply(embed = embed, mention_author=False)
    elif member == 'server':
      embed = discord.Embed(title="Avatar Link",
      url=ctx.guild.icon_url,
      color=ctx.author.top_role.color)
      embed.set_author(name=ctx.guild.name,
      icon_url=ctx.guild.icon_url)
      embed.set_image(url=ctx.guild.icon_url_as(format='gif') if ctx.guild.is_icon_animated() else ctx.guild.icon_url_as(format='png'))
      embed.set_footer(text='Requested by {}'.format(ctx.author),
      icon_url=ctx.author.avatar_url)
      await ctx.reply(embed = embed, mention_author=False)
    elif not ctx.guild.get_member_named(member):
      await ctx.message.add_reaction('❌')
      embed = discord.Embed(description=':rolling_eyes: - {} I can\'t find **{}**!'.format(ctx.author.name, member), color=0xe74c3c)
      await ctx.reply(embed=embed, mention_author=False)
    else:
      member = ctx.guild.get_member_named(member)
      embed = discord.Embed(title="Avatar Link",
      url=member.avatar_url,
      color=member.top_role.color)
      embed.set_author(name=member,
      icon_url=member.avatar_url)
      embed.set_image(url=member.avatar_url_as(format='gif') if member.is_avatar_animated() else member.avatar_url_as(format='png'))
      embed.set_footer(text='Requested by {}'.format(ctx.author),
      icon_url=ctx.author.avatar_url)
      await ctx.reply(embed = embed, mention_author=False)
  else:
    member = ctx.author
    embed = discord.Embed(title="Avatar Link",
    url=member.avatar_url,
    color=member.top_role.color)
    embed.set_author(name=member,
    icon_url=member.avatar_url)
    embed.set_image(url=member.avatar_url_as(format='gif') if member.is_avatar_animated() else member.avatar_url_as(format='png'))
    embed.set_footer(text='Requested by {}'.format(member),
    icon_url=member.avatar_url)
    await ctx.reply(embed = embed, mention_author=False)

#say command
@bot.command(description='Sends the provided message.', aliases=['s'])
@commands.guild_only()
async def say(ctx, *, arg):
  await ctx.message.delete()
  await ctx.trigger_typing()
  await ctx.send(arg)

@say.error
async def say_error(ctx : commands.Context, error : commands.CommandError):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.message.add_reaction('❌')
    embed = discord.Embed(title='Missing Arguments Error', description=':no_entry: - You are missing the required arguments to run this command!', color=0xe74c3c)
    embed.add_field(name='Command:', value='**&say `[message]`**')
    await ctx.send(embed=embed)

#quote command
@bot.command(description='Returns a random quote.')
@commands.guild_only()
async def quote(ctx):
  quote = get_random_quote().split('|')[0]
  author = get_random_quote().split('|')[1]
  await ctx.message.delete()
  await ctx.trigger_typing()
  embed = discord.Embed(title='Quote:',
  description=quote,
  color=ctx.message.author.top_role.color)
  embed.add_field(name='Author:', value=f':book: *{author}*')
  embed.set_footer(text='Requested by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)

#keep_alive()
bot.run(os.getenv('TOKEN'))
