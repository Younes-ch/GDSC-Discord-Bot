from discord.ext import commands
from discord import app_commands
import discord


class MonitorChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.interactions: dict[int, dict[int, discord.Interaction]] = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.interactions[guild.id] = {}

    @app_commands.command(description="Deletes every message sent in the channel except yours and other bots'.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def shut_up(self, interaction: discord.Interaction):
        try:
            if self.interactions[interaction.guild.id][interaction.channel.id]:
                await interaction.response.send_message("I'm already deleting messages in this channel.", ephemeral=True)
                return
        except KeyError:
            self.interactions[interaction.guild.id][interaction.channel.id] = interaction
            await interaction.response.send_message(
                "**================================= 🤫 Please no messages until the vote is over 🤫 =================================**"
            )

    @app_commands.command(description="Stops deleting every message sent in the channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def stop(self, interaction: discord.Interaction):
        try:
            if self.interactions[interaction.guild.id][interaction.channel.id]:
                del self.interactions[interaction.guild.id][interaction.channel.id]
                await interaction.response.send_message(
                    "**===================================== 🤐 You can talk now 🤐 =====================================**"
                )
        except KeyError:
            await interaction.response.send_message("I'm not deleting messages in this channel.", ephemeral=True)
            return

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if (message.type is not discord.MessageType.chat_input_command and self.interactions[message.guild.id].get(message.channel.id)):
            if (message.channel.id == self.interactions[message.guild.id][message.channel.id].channel_id):
                if (message.author != self.interactions[message.guild.id][message.channel.id].user and not message.author.bot):
                    await message.delete()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self.interactions[guild.id] = {}

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        del self.interactions[guild.id]

    @shut_up.error
    @stop.error
    async def shut_up_error(self, interaction: discord.Interaction, error: Exception):
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
    await bot.add_cog(MonitorChat(bot))
