from helpers.my_custom_functions import get_random_joke
from discord.ext import commands
from discord import app_commands
import discord

class Joke(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Returns a random joke. You can also specify a word to search for in the joke.')
    @app_commands.describe(word="The word to search for in the joke. (optional)")
    async def joke(self, interaction: discord.Interaction, word: str = None):
        if word:
            full_joke = get_random_joke(word)
        else:
            full_joke = get_random_joke()
        joke_category = full_joke.split('|')[0]
        joke = full_joke.split('|')[1]
        if joke_category == 'error':
            embed = discord.Embed(description=':no_entry: - {} !'.format(joke), color=0xe74c3c)  
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title='Joke:', description=joke, color=interaction.user.top_role.color)
            embed.add_field(name='Category:', value=f':book: *{joke_category}*')
            embed.set_footer(text='Requested by {}'.format(interaction.user.name), icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Joke(bot))