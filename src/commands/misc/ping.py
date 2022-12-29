from discord.ext import commands
from discord import app_commands
import discord

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Returns the bot\'s latency.')
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(title='🏓 Pong!', description=f'✅ {round(self.bot.latency * 1000)}ms', color=interaction.user.top_role.color)
        embed.set_footer(text='Requested by {}'.format(interaction.user), icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))