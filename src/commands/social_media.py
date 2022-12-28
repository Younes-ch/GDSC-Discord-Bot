from helpers.my_custom_classes import ViewForSocialMediaCommand
from discord.ext import commands
from discord import app_commands
import discord

class SocialMedia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Displays our social media links.')
    async def socialmedia(self, interaction: discord.Interaction):
        view = ViewForSocialMediaCommand(self.bot)
        if interaction.channel.id == 1057448784562499656 or interaction.channel.id == 1057448996274192494:
            await interaction.response.send_message('Here are our social media links:', view=view)
        else:
            await interaction.response.send_message('Here are our social media links:', view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(SocialMedia(bot))
