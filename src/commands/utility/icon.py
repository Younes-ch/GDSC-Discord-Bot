from discord.ext import commands
from discord import app_commands
import discord

class Icon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Returns the server icon.')
    async def icon(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Server Icon:', color=interaction.user.top_role.color, url=interaction.guild.icon.url)
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
        embed.set_image(url=interaction.guild.icon.url)
        embed.set_footer(text='Requested by {}'.format(interaction.user.name), icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Icon(bot))