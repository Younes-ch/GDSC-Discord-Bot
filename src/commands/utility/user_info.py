from discord.ext import commands
from discord import app_commands
import discord

class UserInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.context_menu = app_commands.ContextMenu(name="User information", callback=self.get_user_info)
        self.bot.tree.add_command(self.context_menu)

    @app_commands.command(name='userinfo', description='Display information about a member. yourself if no user is provided.')
    @app_commands.describe(member='The member to get information about. (optional)')
    async def user_info(self, interaction: discord.Interaction, member: discord.Member = None):
        await self.get_user_info(interaction, member)

    async def get_user_info(self, interaction: discord.Interaction, member: discord.Member = None):
        if not member:
            member = interaction.user
        statuses = {
            'online' : '🟢 Online',
            'idle' : '🟠 Idle',
            'dnd' : '⛔ Do not Disturb',
            'offline' : '⚪ Offline',
        }
        guild = interaction.guild
        status = statuses[guild.get_member(member.id).status.name]
        try:
            color = member.top_role.color if member.top_role.color != discord.Color.default() else member.roles[-2].color
        except IndexError:
            color = discord.Color.default()
        embed = discord.Embed(title=member.display_name, color = color)
        embed.add_field(name='ID', value=member.id)
        embed.add_field(name='Avatar:', value="[Link]({})".format(member.display_avatar.url))
        embed.add_field(name='Activity', value=f'{str(member.activity.type).split(".")[-1].title()} **{str(member.activity.name)}**!' if member.activity else 'N/A')
        embed.add_field(name='Bot?', value='✅' if member.bot else '❌')
        embed.add_field(name='Booster', value=member.premium_since.strftime("%d-%b-%Y") if member.premium_since else '❌')
        embed.add_field(name='Status', value=status)
        embed.add_field(name='Created at', value=member.created_at.strftime("%d-%b-%Y"))
        embed.add_field(name='Joined at', value=member.joined_at.strftime("%d-%b-%Y"))
        embed.add_field(name='Top Role', value=member.top_role.mention)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text='Requested by {}'.format(interaction.user.name), icon_url = interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(UserInfo(bot))