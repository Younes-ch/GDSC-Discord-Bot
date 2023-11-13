from helpers.my_custom_functions import get_random_meme
from discord.ext import commands
from discord import app_commands
import discord

class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(description='Returns a random meme from a subreddit.')
    @app_commands.describe(subreddit="The subreddit to get the meme from. (optional)")
    async def meme(self, interaction: discord.Interaction, subreddit: str = None):
        meme = get_random_meme(subreddit).split('|')
        if meme[0] == 'error':
            embed = discord.Embed(description=f':rolling_eyes: - {interaction.user.name} I can\'t find a subreddit named **{subreddit}**', color = 0xe74c3c)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif meme[0] == 'nsfw':
            await interaction.response.send_message('👀 The meme you requested contains **NSFW** content. 👀', ephemeral=True)
        else:
            embed = discord.Embed(title=meme[0], color=interaction.user.top_role.color)
            embed.set_image(url=meme[1])
            embed.add_field(name='Subreddit:', value=meme[2])
            embed.add_field(name='Upvotes:', value=meme[3])
            embed.add_field(name='Post Link:', value=meme[4])
            embed.add_field(name='Post Author:', value=meme[5])
            embed.set_footer(text='Requested by {}'.format(interaction.user.name), icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Meme(bot))
