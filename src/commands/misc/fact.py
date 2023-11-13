from helpers.my_custom_functions import get_random_fact
from discord.ext import commands
from discord import app_commands
import discord

class Fact(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Returns a random fact.')
    async def fact(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Random Fact:', description=get_random_fact(), color=interaction.user.top_role.color)
        embed.set_thumbnail(url='https://image.shutterstock.com/image-illustration/fun-facts-colorful-stripes-260nw-683840437.jpg')
        embed.set_footer(text=f'Requested by {interaction.user.name}', icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Fact(bot))