from helpers.my_custom_functions import get_random_quote
from discord.ext import commands
from discord import app_commands
import discord

class Quote(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Returns a random quote.')
    async def quote(self, interaction: discord.Interaction):
        quote = get_random_quote().split('|')[0]
        author = get_random_quote().split('|')[1]
        embed = discord.Embed(title='Quote:',
        description=quote,
        color=interaction.user.top_role.color)
        embed.add_field(name='Author:', value=f':book: *{author}*')
        embed.set_footer(text='Requested by {}'.format(interaction.user.name), icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Quote(bot))