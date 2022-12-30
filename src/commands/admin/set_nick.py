from discord.ext import commands
from discord import app_commands
import discord

class SetNick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="setnick", description="Changes the nickname of a member.")
    @app_commands.describe(member="The member to change the nickname of.", new_nick="The new nickname for the member. If not provided, the nickname will be removed if it exists.")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    @app_commands.guild_only()
    async def set_nick(self, interaction: discord.Interaction, member: discord.Member, new_nick: str = None):
        await interaction.response.defer(ephemeral=True)
        await member.edit(nick=f'{new_nick or member.name}')
        await interaction.followup.send(f"**✅ - Changed the nickname of {member.mention} to `{new_nick or member.name}`!**")

    @set_nick.error
    async def set_nick_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(title="Missing Permissions", description="⛔ - You don't have the permission to use this command.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error", description="⛔ - An error occured while running the command!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(SetNick(bot))