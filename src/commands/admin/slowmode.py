from helpers.my_custom_classes import ViewForYesOrNoDisableSlowMode
from discord.ext import commands
from discord import app_commands
import discord

class Slowmode(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="slowmode", description="Enable or disable slowmode on a channel.")
    @app_commands.describe(channel="The channel to set the slowmode of. If not provided, the slowmode will be set on the current channel.", seconds="The amount of seconds to set the slowmode to. If not provided, the slowmode will be disabled.")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.guild_only()
    async def slowmode(self, interaction: discord.Interaction, channel: discord.TextChannel = None, seconds: int = None):
        await interaction.response.defer(ephemeral=True)
        if not channel:
            channel = interaction.channel
        if not seconds and channel.slowmode_delay == 0:
            await interaction.followup.send(f"**⛔ - Slowmode is already disabled on {channel.mention}!**")
            return
        if seconds and channel.slowmode_delay == seconds:
            await interaction.followup.send(f"**✅ - Slowmode is already set to `{seconds}s` on {channel.mention}!**")
            return
        elif not seconds and channel.slowmode_delay != 0:
            seconds = channel.slowmode_delay
            view = ViewForYesOrNoDisableSlowMode(interaction, channel)
            await interaction.followup.send(f"**⏱️ - Current slowmode  is set to `{seconds}s` on {channel.mention}!**\nWould you like to disable it?",
                                            view=view)
        else:
            await channel.edit(slowmode_delay=seconds)
            await interaction.followup.send(f"**⏱️ - Set the slowmode of {channel.mention} to `{seconds or 0}s`!**")

    @slowmode.error
    async def slowmode_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(title="Missing Permissions", description="⛔ - You don't have the permission to use this command.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error", description="⛔ - An error occured while running the command!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(error)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Slowmode(bot))