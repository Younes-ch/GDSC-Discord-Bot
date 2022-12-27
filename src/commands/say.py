from discord.ext import commands
from discord import app_commands
import discord

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Sends a message in the same channel. You can also mention the channel to send the message in.')
    @app_commands.describe(message="The message to send.", channel="The channel to send the message in. (optional)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def say(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        await interaction.response.defer(ephemeral=True)
        if channel:
            await interaction.followup.send('Sent the message in {}!'.format(channel.mention), ephemeral=True)
            await channel.send(message)
        else:
            await interaction.followup.send('Sent the message in {}!'.format(interaction.channel.mention), ephemeral=True)
            await interaction.channel.send(message)

    @say.error
    async def say_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(title='Permission Error', description=':no_entry: - You are missing the required permissions to run this command!', color=0xe74c3c)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title='Error', description=':no_entry: - An error occured while running this command!', color=0xe74c3c)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(error)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Say(bot))