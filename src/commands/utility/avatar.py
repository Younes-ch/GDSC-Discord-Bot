from discord.ext import commands
from discord import app_commands
import discord

class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.context_menu = app_commands.ContextMenu(name="Avatar", callback=self.get_avatar)
        self.bot.tree.add_command(self.context_menu)

    @app_commands.command(description='Returns the avatar of a member. You can also mention the member. Yours if none was mentioned.')
    @app_commands.describe(member="The member to get the avatar of. (optional)")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        await self.get_avatar(interaction, member)
    
    async def get_avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        embed = discord.Embed(title="Avatar Link", url=member.display_avatar.url, color=member.top_role.color)
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text='Requested by {}'.format(interaction.user.name), icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Avatar(bot))
