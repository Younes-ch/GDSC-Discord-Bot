from discord.ext import commands
from discord import app_commands
import discord


class MonitorChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.interactions: dict[int, discord.Interaction] = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.interactions[guild.id] = None

    @app_commands.command(description="Deletes every message sent in the channel except yours and other bots'.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def shut_up(self, interaction: discord.Interaction):
        if self.interactions[interaction.guild.id] is not None:
            await interaction.response.send_message(
                "I'm already deleting messages in this channel.", ephemeral=True
            )
            return

        self.interactions[interaction.guild.id] = interaction
        await interaction.response.send_message(
            "**================================= 🤫 Please no messages until the vote is over 🤫 =================================**"
        )

    @app_commands.command(description="Stops deleting every message sent in the channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def stop(self, interaction: discord.Interaction):
        if self.interactions[interaction.guild.id] is None:
            await interaction.response.send_message("I'm not deleting messages in this channel.", ephemeral=True)
            return

        self.interactions[interaction.guild.id] = None
        await interaction.response.send_message(
            "**===================================== 🤐 You can talk now 🤐 =====================================**"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if (message.type is not discord.MessageType.chat_input_command and self.interactions[message.guild.id] is not None):
            if message.channel == self.interactions[message.guild.id].channel:
                if (message.author != self.interactions[message.guild.id].user and not message.author.bot):
                    await message.delete()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.interactions[guild.id] = None

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self.interactions.pop(guild.id)

    @shut_up.error
    @stop.error
    async def shut_up_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.MissingAnyRole):
            await interaction.response.send_message("allah ghaleb sala7iyetik ma7douda. 😏", ephemeral=True)
        else:
            embed = discord.Embed(
                description=":no_entry: An error occured while executing this command. Please try again later.",
                color=0xFF0000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MonitorChat(bot))
