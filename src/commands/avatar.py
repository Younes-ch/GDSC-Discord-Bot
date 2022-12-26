from discord.ext import commands
from discord import app_commands
import discord

class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Returns the avatar of a member. You can also mention the member. Yours if none was mentioned.')
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        embed = discord.Embed(title="Avatar Link", url=member.display_avatar.url, color=member.top_role.color)
        embed.set_author(name=member, icon_url=member.display_avatar.url)
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text='Requested by {}'.format(interaction.user), icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Avatar(bot))