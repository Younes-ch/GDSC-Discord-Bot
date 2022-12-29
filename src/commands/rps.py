from helpers.my_custom_classes import ViewForRPSCommand
from discord.ext import commands
from discord import app_commands
import discord


class RPS(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(description='Play Rock Paper Scissors with your friends!')
    @app_commands.describe(member='The member to play with.')
    async def rps(self, interaction: discord.Interaction, member : discord.Member):
        if interaction.user == member or member.bot:
            raise app_commands.AppCommandError()
        else:
            await interaction.response.defer(thinking=True)
            embed = discord.Embed(title='Rock Paper Scissors:', description='**Who will win? 🤔**', color=interaction.user.top_role.color)
            embed.set_thumbnail(url='https://facts.net/wp-content/uploads/2020/11/rock-paper-scissors.jpg')
            embed.add_field(name='Player 1:', value=interaction.user.name)
            embed.add_field(name='Player 2:', value=member.name)
            await interaction.followup.send(embed=embed)
            embed.description = '**Choose an option from below:**'
            player1_msg = await interaction.user.send(f'You challenged **{member.name}** to a game of **Rock Paper Scissors**!', embed=embed)
            view = ViewForRPSCommand(interaction=interaction, author=interaction.user, member=member, player_msg=player1_msg, embed=embed)
            await player1_msg.edit(view=view)
    
    @rps.error
    async def rps_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.AppCommandError):
            embed = discord.Embed(description=':no_entry: You cannot play against **yourself** or a **bot**!', color=interaction.user.top_role.color)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description=':no_entry: An error occurred while executing this command.', color=interaction.user.top_role.color)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(RPS(bot))