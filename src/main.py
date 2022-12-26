from PIL import Image, ImageFont, ImageDraw
from helpers.my_custom_functions import find_invite_by_code
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import tasks
import discord
import discord
import asyncio
import os

class Bot(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix='&', intents=discord.Intents.all(), activity=discord.Activity(type=discord.ActivityType.listening, name="/help"),
    help_command=None)
    self.available_commands = [
                               "commands.quote", "commands.joke", "commands.icon", "commands.avatar", "commands.ping",
                               "commands.user_info", "commands.corona", "commands.server_info", "commands.meme", "commands.fact",
                               "commands.say", "commands.announce", "commands.weather", "commands.help", "commands.rps", "commands.question",
                            ]
    self.invites = {}

  async def setup_hook(self):
    for ext in self.available_commands:
      await self.load_extension(ext)
      print(f"Loaded \033[33m{ext.replace('commands.', '')}.py\033[0m")

  async def on_ready(self):
    print('------')
    print('Logged in as:')
    print(self.user.name)
    print(self.user.id)
    print('------')
    try:
      synced = await self.tree.sync()
      print(f"Synced {len(synced)} command(s):")
      for command in synced:
        print('\033[33m', command.name, '\33[0m-->', command.description)
    except Exception as e:
      print(e)
    self.member_count.start()
    for guild in self.guilds:
      if not guild.id in [828940910053556224, 783404400416391189]:
        await guild.owner.send(':rolling_eyes: Sorry, I left `{}` because I\'m a private bot that only works in `GDSC ISSATSo Community Server!`'.format(guild.name))
        await guild.leave()
      else:
        self.invites[guild.id] = await guild.invites()

  async def on_member_join(self, member):
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

      self.invites
      invites_before_join = self.invites[member.guild.id]
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
            self.invites[member.guild.id] = invites_after_join

  async def on_member_update(self, before, after):
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

  async def on_member_remove(self, member):
    self.invites[member.guild.id] = await member.guild.invites()

  async def on_guild_join(self, guild):
    if not guild.id in [828940910053556224, 783404400416391189]:
      await guild.owner.send(f':rolling_eyes: Sorry, I left `{guild.name}` because I\'m a private bot that only works in `GDSC ISSATSo Community Server!`')
      await guild.leave()

  @tasks.loop(seconds=30.0)
  async def member_count(self):
    for guild in self.guilds:
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

# -------------------------------------------- Run Bot -------------------------------------------- #
bot = Bot()
load_dotenv()
bot.run(os.getenv('TOKEN'))
