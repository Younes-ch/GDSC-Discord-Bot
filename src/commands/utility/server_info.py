from discord.ext import commands
from discord import app_commands
import discord

class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='serverinfo', description='Display information about the server.')
    async def server_info(self, interaction: discord.Interaction):
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

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfo(bot))