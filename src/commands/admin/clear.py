from discord.ext import commands
from discord import app_commands
import discord


class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    @app_commands.command(description="Cleans messages from a channel.")
    @app_commands.describe(number_of_messages="Number of messages to delete.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, number_of_messages: int,
                        filter_by_user: discord.Member = None,
                        filter_by_role: discord.Role = None,
                        filter_by_bot: bool = False):
        

        if number_of_messages <= 0:
            await interaction.response.send_message("```diff\n- The number of messages to delete must be greater than 0.```", ephemeral=True)
            return

        channel = interaction.channel
        messages = [message async for message in channel.history(limit=number_of_messages) if self.check(message, filter_by_user, filter_by_role, filter_by_bot)]
        if len(messages) == 0:
            await interaction.response.send_message(f"```ini\n[No messages found.] matching the criteria specified in the last [{number_of_messages}] messages.```", delete_after=5)
            return
        for message in messages:
            await message.delete()
        await interaction.response.send_message(f"```ini\n[{len(messages)}] messages has been deleted.```", delete_after=5)
    

    def check(self, message: discord.Message, filter_by_user: discord.Member, filter_by_role: discord.Role, filter_by_bot: bool):
        if filter_by_user and filter_by_role:
            return message.author == filter_by_user and filter_by_role in message.author.roles
        elif filter_by_user:
            return message.author == filter_by_user
        elif filter_by_role:
            return filter_by_role in message.author.roles
        elif filter_by_bot:
            return message.author.bot
        else:
            return True
        
    @clear.error
    async def clear_error(self, interaction: discord.Integration, error: Exception):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(
                title="Permission Error",
                description=":no_entry: - You are missing the required permissions to run this command!",
                color=0xCA3B3B,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                description=":no_entry: An error occured while executing this command. Please try again later.",
                color=0xFF0000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Clear(bot))
