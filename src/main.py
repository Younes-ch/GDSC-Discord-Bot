import time
from helpers.my_custom_functions import find_invite_by_code, get_corresponding_server_logs_channel_id
from helpers.my_custom_classes import ViewForSocialMediaCommand
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import tasks
import datetime
import discord
import asyncio
import os

class Bot(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix='&', intents=discord.Intents.all(), activity=discord.Activity(type=discord.ActivityType.listening, name="/help"),
    help_command=None)
    self.invites = {}
    self.guild_members = {}
    self.guild_voice_channels = {}
    self.server_stats_category_channel = {}

  async def setup_hook(self):
    groups = [folder for folder in os.listdir('src/commands') if folder != '__pycache__']
    for group in groups:
      extensions = [ext for ext in os.listdir(f'src/commands/{group}') if ext != '__pycache__']
      for ext in extensions:
        await self.load_extension(f'commands.{group}.{ext.replace(".py", "")}')
        print(f"Loaded \033[33m{ext}\033[0m")
    self.add_view(ViewForSocialMediaCommand(self))

  async def on_ready(self):
    print('------')
    print('Logged in as:')
    print(self.user.name)
    print(self.user.id)
    print('------')
    try:
      synced = await self.tree.sync()
      synced = [command for command in synced if command.description]
      print(f"Synced {len(synced)} command(s):")
      for command in synced:
        print('\033[33m', command.name, '\33[0m-->', command.description)
    except Exception as e:
      print(e)

   
    
    category_name = "╭─── 𝚂𝚎𝚛𝚟𝚎𝚛 𝚂𝚝𝚊𝚝𝚜 📊 ───╮"

    for guild in self.guilds:
      if guild.id not in [828940910053556224, 783404400416391189]:
        await guild.owner.send(':rolling_eyes: Sorry, I left `{}` because I\'m a private bot that only works in `GDSC ISSATSo Community Server!`'.format(guild.name))
        await guild.leave()
      else:
        overwrites = {
          guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False)
        }
        guild_categories = guild.categories

        if category_name not in [category.name for category in guild_categories]:
          self.server_stats_category_channel[guild.id] = await guild.create_category(name=category_name, overwrites=overwrites, position=0)
        else:
          self.server_stats_category_channel[guild.id] = list(filter(lambda category: category.name == category_name, guild_categories))[0]

        self.guild_members[guild.id] = list(guild.members)
        self.guild_voice_channels[guild.id] = guild.voice_channels
        self.invites[guild.id] = await guild.invites()
        await self.update_member_count(guild)
    # self.update_time_channel.start()
    self.update_member_status_count.start()
    self.update_date_channel.start()

# ********************************************************* Messages Events ***************************************************************
  async def on_message_edit(self, before: discord.Message, after: discord.Message):
    if before.author.bot:
      return
    if before.content != after.content:
      server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(before.guild.id))
      embed = discord.Embed(description=f'✏️ **Message sent by {before.author.mention} edited in {before.channel.mention}.**\n[Jump to message]({after.jump_url})',
                            color=0xf1c40f,
                            timestamp=datetime.datetime.utcnow())
      embed.set_author(name=before.author.name, icon_url=before.author.display_avatar.url)
      embed.add_field(name='Old:', value=f'```{before.content}```', inline=False)
      embed.add_field(name='New:', value=f'```{after.content}```', inline=False)
      embed.set_footer(text=before.guild.name)
      embed.timestamp = datetime.datetime.utcnow()
      await server_logs_channel.send(embed=embed)

  async def on_message_delete(self, message: discord.Message):
    if message.content and message.guild:
      server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(message.guild.id))
      embed = discord.Embed(description=f'🗑️ **Message sent by {message.author.mention} deleted in {message.channel.mention}.**',
                            color=0xca3b3b,
                            timestamp=datetime.datetime.utcnow())
      embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
      embed.add_field(name='Message Content', value=f'{message.content}', inline=False)
      embed.set_footer(text=message.guild.name)
      await server_logs_channel.send(embed=embed)

# ********************************************************* Member Events ***************************************************************

  async def on_member_join(self, member: discord.Member):
    self.guild_members[member.guild.id].append(member)

    if not member.bot:
      users_count_channel = [vc for vc in self.guild_voice_channels[member.guild.id] if vc.name.startswith('Users')][0]
      await self.update_member_count(member.guild, users_count_channel)
    else:
      bots_count_channel = [vc for vc in self.guild_voice_channels[member.guild.id] if vc.name.startswith('Bots')][0]
      await self.update_member_count(member.guild, bots_count_channel)

    if member.guild.id == 828940910053556224:
      welcome_channel = self.get_channel(935969094652551189)
      invites_channel = self.get_channel(940729129689554944)
    else:
      welcome_channel = self.get_channel(783406528165838888)
      rules_channel = self.get_channel(841102973206659134)
      invites_channel = self.get_channel(941418127261040720)
      if not member.bot:
        await rules_channel.send(member.mention, delete_after=0.1)
        await member.add_roles(member.guild.get_role(835557953057718314), reason="New User")
        await member.add_roles(member.guild.get_role(918937715217690634), reason="New User")
      else:
        await member.add_roles(member.guild.get_role(835602765048840252), reason="New Bot")

    if not member.bot:
      avatar_file_name = "avatar.png"
      await member.display_avatar.save(avatar_file_name)
      avatar = Image.open("avatar.png")
      avatar = avatar.resize((148, 140))

      mask_im = Image.new("L", avatar.size, 0)
      draw = ImageDraw.Draw(mask_im)
      draw.ellipse((0, 0, 148, 140), fill=255, outline=0, width=2)
      mask_im.save('mask_circle.png', quality=95)

      background = Image.open('src/assets/GDSC Welcome Template.png')
      font = ImageFont.truetype("src/assets/Google-Sans.ttf", 54)
      background_copy = background.copy()
      background_copy.paste(avatar, (951, 596), mask_im)
      draw = ImageDraw.Draw(background_copy)
      margin = 410 if len(member.name) == 2 else (410 - ((len(member.name)/2) * 20))
      draw.text((margin, 407), '{}'.format(member.display_name), (231, 245, 254), font=font)
      
      background_copy.save("member_landed.png")

      await welcome_channel.send(content=f'Welcome {member.mention} to **GDSC ISSATSo Community Server**. *Enjoy your stay!*', file=discord.File("member_landed.png"))
      await asyncio.sleep(1)
      os.remove("member_landed.png")
      os.remove("avatar.png")
      os.remove('mask_circle.png')

      invites_before_join: list[discord.Invite] = self.invites[member.guild.id]
      invites_after_join: list[discord.Invite] = await member.guild.invites()

      for invite in invites_before_join:
        if find_invite_by_code(invites_after_join, invite.code):
          if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
            embed = discord.Embed(description=f'📥 **{member.mention} has joined the server**', color=0x2ecc71, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f'{member.name}', icon_url=member.display_avatar.url)
            embed.add_field(name='🔒 Invite Code:', value=invite.code)
            embed.add_field(name='✉️ Inviter:', value=invite.inviter.name)
            embed.set_footer(text=f'Guild: {member.guild.name}', icon_url=member.guild.icon.url)
            embed.set_thumbnail(url=member.display_avatar.url)
            await asyncio.sleep(2)
            await invites_channel.send(embed=embed)
            self.invites[member.guild.id] = invites_after_join
      
      server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(member.guild.id))
      embed = discord.Embed(description=f'📥 **{member.mention} has joined the server**', color=0x2ecc71, timestamp=datetime.datetime.utcnow())
      embed.set_author(name=f'{member.name}', icon_url=member.display_avatar.url)
      embed.add_field(name='Account Creation:', value=member.created_at.strftime('%d %B %Y, %I:%M %p'))
      embed.add_field(name='Joined At:', value=member.joined_at.strftime('%d %B %Y, %I:%M %p'))
      embed.set_footer(text=f'{member.guild.name} • User ID: {member.id}', icon_url=member.guild.icon.url)
      embed.set_thumbnail(url=member.display_avatar.url)
      await server_logs_channel.send(embed=embed)

  async def on_member_update(self, before: discord.Member, after: discord.Member):
    before_roles = [role.name for role in before.roles]
    after_roles = [role.name for role in after.roles]
    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(after.guild.id))
    self.guild_members[after.guild.id] = [after if member.id == after.id else member for member in self.guild_members[after.guild.id]]

    if len(before_roles) < len(after_roles):
      if "Event Speaker" not in before_roles and "Event Speaker" in after_roles:
        if "Event Speaker" not in after.display_name:
          try:
            await after.edit(nick=f'[Event Speaker] {before.display_name}')
          except discord.errors.Forbidden:
            await after.send(f'**Event Speaker** Role has just been __added__ to your roles in **{after.guild.name}** server, please go ahead and add **[Event Speaker]** *tag* to your nickname')
      embed = discord.Embed(description=f'🔧 **{after.mention} has been given a new role**', color=0xf1c40f, timestamp=datetime.datetime.utcnow())
      embed.set_author(name=f'{after.name}', icon_url=after.display_avatar.url)
      embed.add_field(name='✅ Added role:', value=list(filter(lambda x: x not in before_roles, after_roles))[0])
      embed.set_footer(text=f'User ID: {after.id}')
      embed.set_thumbnail(url=after.display_avatar.url)
      await server_logs_channel.send(embed=embed)
    elif len(before_roles) > len(after_roles):
      if "Event Speaker" in before_roles and "Event Speaker" not in after_roles:
        if "[Event Speaker]" in after.display_name:
          try:
            new_nick = after.display_name.replace("[Event Speaker]", "")
            await after.edit(nick=new_nick)
          except discord.errors.Forbidden:
            await after.send(f'**Event Speaker** Role has just been __removed__ from your roles in **{after.guild.name}** server, please go ahead and remove **[Event Speaker]** *tag* from your nickname')      
      embed = discord.Embed(description=f'🔧 **{after.mention} has lost a role**', color=0xf1c40f, timestamp=datetime.datetime.utcnow())
      embed.set_author(name=f'{after.name}', icon_url=after.display_avatar.url)
      embed.add_field(name='❌ Removed role:', value=list(filter(lambda x: x not in after_roles, before_roles))[0])
      embed.set_footer(text=f'User ID: {after.id}')
      embed.set_thumbnail(url=after.display_avatar.url)
      await server_logs_channel.send(embed=embed)
    elif before.display_name != after.display_name:
      embed = discord.Embed(description=f'🔧 **{after.mention} has changed their nickname**', color=0xf1c40f, timestamp=datetime.datetime.utcnow())
      embed.set_author(name=f'{after.name}', icon_url=after.display_avatar.url)
      embed.add_field(name='Old nickname:', value=f'`{before.display_name}`')
      embed.add_field(name='New nickname:', value=f'`{after.display_name}`')
      embed.set_footer(text=f'User ID: {after.id}')
      embed.set_thumbnail(url=after.display_avatar.url)
      await server_logs_channel.send(embed=embed)
    elif before.display_avatar.key != after.display_avatar.key:
      embed = discord.Embed(description=f'🔧 **{after.mention} has changed their avatar**', color=0xf1c40f, timestamp=datetime.datetime.utcnow())
      embed.set_author(name=f'{after.name}', icon_url=after.display_avatar.url)
      embed.add_field(name='Old avatar:', value=f'[Before]({before.display_avatar.url})')
      embed.add_field(name='New avatar:', value=f'[After]({after.display_avatar.url})')
      embed.set_footer(text=f'User ID: {after.id}')
      embed.set_thumbnail(url=after.display_avatar.url)
      await server_logs_channel.send(embed=embed)

  async def on_user_update(self, before: discord.User, after: discord.User):
    if before.display_avatar.key != after.display_avatar.key:
      for mutual_guild in after.mutual_guilds:
        server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(mutual_guild.id))
        embed = discord.Embed(description=f'🔧 **{after.mention} has changed their avatar**', color=0xf1c40f, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f'{after.name}', icon_url=before.display_avatar.url)
        embed.add_field(name='Old avatar:', value=f'[Before]({before.display_avatar.url})')
        embed.add_field(name='New avatar:', value=f'[After]({after.display_avatar.url})')
        embed.set_footer(text=f'User ID: {after.id}')
        embed.set_thumbnail(url=after.display_avatar.url)
        await server_logs_channel.send(embed=embed)
          
  async def on_member_remove(self, member: discord.Member):
    self.guild_members[member.guild.id].remove(member)

    if member.bot:
      bots_count_channel = [vc for vc in self.guild_voice_channels[member.guild.id] if vc.name.startswith('Bots')][0]
      await self.update_member_count(member.guild, bots_count_channel)
    else:
      users_count_channel = [vc for vc in self.guild_voice_channels[member.guild.id] if vc.name.startswith('Users')][0]
      await self.update_member_count(member.guild, users_count_channel)

    self.invites[member.guild.id] = await member.guild.invites()
    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(member.guild.id))

    embed = discord.Embed(description=f'📤 **{member.mention} has left the server**', color=0xca3b3b, timestamp=datetime.datetime.utcnow())
    embed.set_author(name=f'{member.name}', icon_url=member.display_avatar.url)
    embed.set_footer(text=f'User ID: {member.id}', icon_url=member.guild.icon.url)
    embed.set_thumbnail(url=member.display_avatar.url)
    await server_logs_channel.send(embed=embed)

  async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(member.guild.id))
    if before.channel is None and after.channel is not None:
      embed = discord.Embed(description=f'📥 **{member.mention} joined voice channel `{after.channel.name}`**', color=0x2ecc71, timestamp=datetime.datetime.utcnow())
      embed.set_author(name=f'{member.name}', icon_url=member.display_avatar.url)
      await server_logs_channel.send(embed=embed)
    elif before.channel is not None and after.channel is None:
      embed = discord.Embed(description=f'📤 **{member.mention} left voice channel `{before.channel.name}`**', color=0xca3b3b, timestamp=datetime.datetime.utcnow())
      embed.set_author(name=f'{member.name}', icon_url=member.display_avatar.url)
      await server_logs_channel.send(embed=embed)
    elif before.channel is not None and after.channel is not None and before.channel.id != after.channel.id:
      embed = discord.Embed(description=f'🔁 **{member.mention} has switched voice channels**', color=0x3498db, timestamp=datetime.datetime.utcnow())
      embed.set_author(name=f'{member.name}', icon_url=member.display_avatar.url)
      embed.add_field(name='Voice channel:', value=f'{before.channel.mention} ➡️ {after.channel.mention}')
      await server_logs_channel.send(embed=embed)

# ********************************************************* Tasks ***************************************************************
  
  @tasks.loop(time=datetime.time(hour=0, minute=0, second=0, tzinfo=datetime.timezone(datetime.timedelta(hours=1))))
  async def update_date_channel(self):
    for guild in self.guilds:
      current_time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=1)))
      possible_channels = [vc for vc in self.guild_voice_channels[guild.id] if vc.name.startswith('📅')]
      if not possible_channels:
        await guild.create_voice_channel(name=f'📅 {current_time.strftime("%d %B %Y")}', category=self.server_stats_category_channel[guild.id])
      else:
        channel = possible_channels[0]
        await channel.edit(name=f'📅 {current_time.strftime("%d %B %Y")}', category=self.server_stats_category_channel[guild.id])
    print(f'Updated Date Channel at: {current_time.strftime("%d %B %Y - %I:%M:%S %p")}')

  @tasks.loop(minutes=1)
  async def update_time_channel(self):
    correct_timezone = datetime.timezone(datetime.timedelta(hours=1))
    current_time = datetime.datetime.now(correct_timezone)

    for guild in self.guilds:
      possible_channels = [vc for vc in self.guild_voice_channels[guild.id] if vc.name.startswith('⏰')]
      if not possible_channels:
        await guild.create_voice_channel(name=f'⏰ {current_time.strftime("%I:%M %p")}', category=self.server_stats_category_channel[guild.id])
      else:
        channel = possible_channels[0]
        await channel.edit(name=f'⏰ {current_time.strftime("%I:%M %p")}', category=self.server_stats_category_channel[guild.id])
   

  @tasks.loop(minutes=10)
  async def update_member_status_count(self):
    current_time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=1)))
    for guild in self.guilds:
      guild_members = self.guild_members[guild.id]

      online_user_count = len(list(filter(lambda member: not member.bot and member.status == discord.Status.online, guild_members)))
      dnd_user_count = len(list(filter(lambda member: not member.bot and member.status == discord.Status.dnd, guild_members)))
      idle_user_count = len(list(filter(lambda member: not member.bot and member.status == discord.Status.idle, guild_members)))

      possible_channels = [vc for vc in self.guild_voice_channels[guild.id] if vc.name.startswith('🟢')]
      if not possible_channels:
        await guild.create_voice_channel(name=f'🟢 {online_user_count} ⛔ {dnd_user_count} 🌙 {idle_user_count}',
                                         category=self.server_stats_category_channel[guild.id])
      else:
        channel = possible_channels[0]
        await channel.edit(name=f'🟢 {online_user_count} ⛔ {dnd_user_count} 🌙 {idle_user_count}', category=self.server_stats_category_channel[guild.id])
    print(f'Updated User status Channel at: {current_time.strftime("%d %B %Y - %I:%M:%S %p")}')
        
  async def update_member_count(self, guild: discord.Guild, channel: discord.VoiceChannel = None):
    
      guild_members = self.guild_members[guild.id]
      current_user_count = len(list(filter(lambda member: not member.bot, guild_members)))
      current_bot_count = guild.member_count - current_user_count

      if not channel:
        possible_channels = [vc for vc in self.guild_voice_channels[guild.id] if vc.name.startswith('Users')]
        if not possible_channels:
          await guild.create_voice_channel(name=f'Users: {current_user_count}', category=self.server_stats_category_channel[guild.id])
        else:
          channel = possible_channels[0]
          await channel.edit(name=f'Users: {current_user_count}', category=self.server_stats_category_channel[guild.id])
        
        possible_channels = [vc for vc in self.guild_voice_channels[guild.id] if vc.name.startswith('Bots')]
        if not possible_channels:
          await guild.create_voice_channel(name=f'Bots: {current_bot_count}', category=self.server_stats_category_channel[guild.id])
        else:
          channel = possible_channels[0]
          await channel.edit(name=f'Bots: {current_bot_count}', category=self.server_stats_category_channel[guild.id])
        
      else:
        if channel.name.startswith('Users'):
          await channel.edit(name=f'Users: {current_user_count}', category=self.server_stats_category_channel[guild.id])
        elif channel.name.startswith('Bots'):
          await channel.edit(name=f'Bots: {current_bot_count}', category=self.server_stats_category_channel[guild.id])

# **************************************************************************************************************************


# ****************************************************** Guild Events ******************************************************

  async def on_guild_join(self, guild):
    if not guild.id in [828940910053556224, 783404400416391189]:
      await guild.owner.send(f':rolling_eyes: Sorry, I left `{guild.name}` because I\'m a private bot that only works in `GDSC ISSATSo Community Server!`')
      await guild.leave()
  
  async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):

    if channel.name.startswith(('📅', '⏰', '🟢', 'Users', 'Bots')):
      if [vc for vc in self.guild_voice_channels[channel.guild.id] if vc.name.startswith(channel.name.split(' ')[0])]:
        await channel.delete()
        return
      self.guild_voice_channels[channel.guild.id].append(channel)
      return
    
    if isinstance(channel, discord.VoiceChannel):
      self.guild_voice_channels[channel.guild.id].append(channel)


    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(channel.guild.id))
    if isinstance(channel, discord.VoiceChannel):
      channel_type = 'Voice Channel'
    elif isinstance(channel, discord.TextChannel):
      channel_type = 'Text Channel'
    elif isinstance(channel, discord.CategoryChannel):
      channel_type = 'Category'
    elif isinstance(channel, discord.StageChannel):
      channel_type = 'Stage'
    elif isinstance(channel, discord.ForumChannel):
      channel_type = 'Forum'

    embed = discord.Embed(description=f'🆕 **{channel_type} has been created**', color=0x2ecc71, timestamp=datetime.datetime.utcnow())
    embed.add_field(name='Name:', value=f'`{channel.name}`')
    if isinstance(channel, discord.VoiceChannel):
      embed.add_field(name='User limit:', value=f'`{channel.user_limit}`')
    if channel.category:
      embed.add_field(name='Category:', value=f'`{channel.category}`')
    embed.set_footer(text=f'Channel ID: {channel.id}')
    await server_logs_channel.send(embed=embed)

  async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(after.guild.id))
    if isinstance(before, discord.VoiceChannel):
      channel_type = 'Voice Channel'
      self.guild_voice_channels[after.guild.id] = [after if vc.id == before.id else vc for vc in self.guild_voice_channels[after.guild.id]]

    elif isinstance(before, discord.TextChannel):
      channel_type = 'Text Channel'
    elif isinstance(before, discord.CategoryChannel):
      channel_type = 'Category'
      if after.name == "╭─── 𝚂𝚎𝚛𝚟𝚎𝚛 𝚂𝚝𝚊𝚝𝚜 📊 ───╮" and (before.position != after.position):
        await after.edit(position=0)
        self.server_stats_category_channel[after.guild.id] = after
        return
    elif isinstance(before, discord.StageChannel):
      channel_type = 'Stage'
    elif isinstance(before, discord.ForumChannel):
      channel_type = 'Forum'

    embed = discord.Embed(color=0xf1c40f, timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f'Channel ID: {before.id}')

    if before.name != after.name:
      if after.name.startswith(('📅', '⏰', '🟢')):
        return
      embed.description = f'🔧 **{channel_type} name has been updated**:'
      embed.add_field(name='Old name:', value=before.name)
      embed.add_field(name='New name:', value=after.name)
      await server_logs_channel.send(embed=embed)
    elif isinstance(before, (discord.VoiceChannel, discord.TextChannel)) and before.category != after.category:
      if after.name.startswith(('📅', '⏰', '🟢', 'Users', 'Bots')):
        return
      embed.description = f'🔧 **{channel_type} category has been updated**: `{after.name}`'
      embed.add_field(name='Old category:', value=before.category)
      embed.add_field(name='New category:', value=after.category)
      await server_logs_channel.send(embed=embed)
      
      if isinstance(before, discord.VoiceChannel):      
        if before.user_limit != after.user_limit:
          embed.description = f'🔧 **{channel_type} user limit has been updated**: `{after.name}`'
          embed.add_field(name='Old user limit:', value=f'{before.user_limit} users')
          embed.add_field(name='New user limit:', value=f'{after.user_limit} users')
          await server_logs_channel.send(embed=embed)
      elif isinstance(before, discord.TextChannel):
        if before.slowmode_delay != after.slowmode_delay:
          embed.description = f'🔧 **{channel_type} slowmode delay has been updated**: `{after.name}`'
          embed.add_field(name='Old delay:', value=f'{before.slowmode_delay}s' if before.slowmode_delay else 'No slowmode delay')
          embed.add_field(name='New dalay:', value=f'{after.slowmode_delay}s' if after.slowmode_delay else 'No slowmode delay')
          await server_logs_channel.send(embed=embed)
        elif before.topic != after.topic:
          embed.description = f'🔧 **{channel_type} topic has been updated**: `{after.name}`'
          embed.add_field(name='Old topic:', value=before.topic if before.topic else 'No topic')
          embed.add_field(name='New topic:', value=after.topic if after.topic else 'No topic')
          await server_logs_channel.send(embed=embed)
  
  async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):

    if isinstance(channel, discord.VoiceChannel):
      self.guild_voice_channels[channel.guild.id].remove(channel)
      if channel.name.startswith(('📅', '⏰', '🟢', 'Users', 'Bots')):
        if channel.name.startswith('Users') or channel.name.startswith('Bots'):
          await self.update_member_count(channel.guild)
        elif channel.name.startswith('🟢'):
          await self.update_member_status_count.__call__()
        elif channel.name.startswith('📅'):
          await self.update_date_channel.__call__()
        elif channel.name.startswith('⏰'):
          await self.update_time_channel.__call__()
        return
    
    if channel.name.startswith("╭─── 𝚂𝚎𝚛𝚟𝚎𝚛 𝚂𝚝𝚊𝚝𝚜 📊 ───╮"):
      overwrites = {
          channel.guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False)
        }
      
      self.server_stats_category_channel[channel.guild.id] = await channel.guild.create_category(name="╭─── 𝚂𝚎𝚛𝚟𝚎𝚛 𝚂𝚝𝚊𝚝𝚜 📊 ───╮", overwrites=overwrites, position=0)

    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(channel.guild.id))
    if isinstance(channel, discord.VoiceChannel):
      channel_type = 'Voice Channel'
    elif isinstance(channel, discord.TextChannel):
      channel_type = 'Text Channel'
    elif isinstance(channel, discord.CategoryChannel):
      channel_type = 'Category'
    elif isinstance(channel, discord.StageChannel):
      channel_type = 'Stage'
    elif isinstance(channel, discord.ForumChannel):
      channel_type = 'Forum'

    embed = discord.Embed(description=f'🗑️ **{channel_type} has been deleted**', color=0xca3b3b, timestamp=datetime.datetime.utcnow())
    embed.add_field(name='Name:', value=f'`{channel.name}`')
    embed.set_footer(text=f'Channel ID: {channel.id}')
    await server_logs_channel.send(embed=embed)

  async def on_guild_role_create(self, role: discord.Role):
    await asyncio.sleep(60)
    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(role.guild.id))
    embed = discord.Embed(description='🆕 **Role has been created**', color=0x2ecc71, timestamp=datetime.datetime.utcnow())
    embed.add_field(name='🏷️ Name:', value=f'`{role.name}`')
    embed.add_field(name='🪪 ID:', value=f'`{role.id}`')
    embed.add_field(name='🎨 Color:', value=f'`#{role.color.value:0>6x}`')
    embed.set_footer(text=role.guild.name)
    await server_logs_channel.send(embed=embed)

  async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
    await asyncio.sleep(60)
    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(before.guild.id))
    embed = discord.Embed(description='🔧 **Role has been updated**', color=0xf1c40f, timestamp=datetime.datetime.utcnow())
    embed.add_field(name='🏷️ Name:', value=f'`{after.name}`')
    embed.add_field(name='🪪 ID:', value=f'`{after.id}`')
    embed.add_field(name='\u200b', value='\u200b')
    embed.set_footer(text=before.guild.name)

    if before.name != after.name or before.color != after.color:
      if before.name != after.name:
        embed.add_field(name='⏮️ Old name:', value=f'`{before.name}`')
        embed.add_field(name='⏭️ New name:', value=f'`{after.name}`')
        embed.add_field(name='\u200b', value='\u200b')
      if before.color != after.color:
        embed.add_field(name='⏮️ Old color:', value=f'`#{before.color.value:0>6x}`')
        embed.add_field(name='⏭️ New color:', value=f'`#{after.color.value:0>6x}`')
        embed.add_field(name='\u200b', value='\u200b')
      await server_logs_channel.send(embed=embed)

  async def on_guild_role_delete(self, role: discord.Role):
    await asyncio.sleep(60)
    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(role.guild.id))
    embed = discord.Embed(description='🗑️ **Role has been deleted**', color=0xca3b3b, timestamp=datetime.datetime.utcnow())
    embed.add_field(name='🏷️ Name:', value=f'`{role.name}`')
    embed.add_field(name='🪪 ID:', value=f'`{role.id}`')
    embed.add_field(name='🎨 Color:', value=f'`#{role.color.value:0>6x}`')
    embed.set_footer(text=role.guild.name)
    await server_logs_channel.send(embed=embed)

  async def on_guild_emojis_update(self, guild: discord.Guild, before: list[discord.Emoji], after: list[discord.Emoji]):
    server_logs_channel = self.get_channel(get_corresponding_server_logs_channel_id(guild.id))
    embed = discord.Embed(timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f'{guild.name}')
    if len(before) < len(after):
      embed.description = '🆕 **Emoji has been added**'
      embed.color = 0x2ecc71
      for emoji in after:
        if emoji not in before:
          embed.add_field(name='🏷️ Name:', value=f'`{emoji.name}`')
          embed.add_field(name='🪪 ID:', value=f'`{emoji.id}`')
          embed.set_thumbnail(url=emoji.url)
          await server_logs_channel.send(embed=embed)
    elif len(before) > len(after):
      embed.description = '🗑️ **Emoji has been deleted**'
      embed.color = 0xca3b3b
      for emoji in before:
        if emoji not in after:
          embed.add_field(name='🏷️ Name:', value=f'`{emoji.name}`')
          embed.add_field(name='🪪 ID:', value=f'`{emoji.id}`')
          embed.set_thumbnail(url=emoji.url)
          await server_logs_channel.send(embed=embed)

# **************************************************************************************************************************************

# -------------------------------------------- Run Bot -------------------------------------------- #
bot = Bot()
load_dotenv()
bot.run(os.getenv('TOKEN'))
