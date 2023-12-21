from discord.ext import commands
from discord import app_commands
from discord.ext import tasks
import datetime
import discord

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipes = {}
        self.clear_snipes.start()
    
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id in self.snipes:
            self.snipes[message.channel.id].append(message)
        else:
            self.snipes[message.channel.id] = [message]

    @app_commands.command(description="Retrieves the last deleted messages in the channel")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def snipe(self, interaction: discord.Interaction):
        channel: discord.TextChannel = interaction.channel
        if channel.id in self.snipes:
            messages: list[discord.Message] = self.snipes[channel.id]
            if messages:
                embed = discord.Embed(title="🗑️ Last deleted messages:", color=0xca3b3b, timestamp=datetime.datetime.utcnow())
                for message in messages[-min(10, len(messages)):]:
                    embed.add_field(name=f"**Message sent by `{message.author.name}`:**",
                                    value=f'💬 {message.content}\nCreated at: {message.created_at.strftime("%d-%b-%Y %H:%M:%S")}', inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("There are no deleted messages in this channel", ephemeral=True)
        else:
            await interaction.response.send_message("There are no deleted messages in this channel", ephemeral=True)
    
    @snipe.error
    async def snipe_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(
                                    title='Permission Error',
                                    description=':no_entry: - You are missing the required permissions to run this command!',
                                    color=0xca3b3b
                                )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                                    description=':no_entry: - An error occured while running this command!',
                                    color=0xca3b3b
                                )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @tasks.loop(minutes=10)
    async def clear_snipes(self):
        for channel_id in self.snipes:
            messages = self.snipes[channel_id]
            self.snipes[channel_id] = messages[-min(10, len(messages)):]
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Snipe(bot))

