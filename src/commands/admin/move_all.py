from discord.ext import commands
from discord import app_commands
from discord.ext import tasks
import discord

class MoveAll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.connected_voice_channels = {
            828940910053556224: None,
            783404400416391189: None
        }
        self.interaction: discord.Interaction = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id == self.bot.user.id:
            if before.channel is None and after.channel is not None:
                    self.disconnect_after_inactivity.start()
                    self.connected_voice_channels[member.guild.id] = after.channel
            elif before.channel is not None and after.channel is None:
                    self.disconnect_after_inactivity.stop()
                    self.connected_voice_channels[member.guild.id] = None
                    self.interaction_channel = None
            elif before.channel is not None and after.channel is not None and before.channel.id != after.channel.id:
                    self.connected_voice_channels[member.guild.id] = after.channel
                    if before.channel.members:
                        for member in before.channel.members:
                            await member.move_to(after.channel)
                        await self.interaction.followup.send(f"**✅ - Moved everyone to {after.channel.mention}!**", ephemeral=True)
                    else:
                        await self.interaction.followup.send("**❌ - There were no members in the voice channel.**", ephemeral=True)
                

    @app_commands.command(description="Moves everyone in a voice channel to another voice channel")
    @app_commands.describe(voice_channel="The voice channel that the bot will join. If not specified, the bot will join your voice channel.")
    @app_commands.checks.has_permissions(move_members=True)
    @app_commands.guild_only()
    async def moveall(self, interaction: discord.Interaction, voice_channel: discord.VoiceChannel = None):
        if not interaction.user.voice and not voice_channel:
            return await interaction.response.send_message("**❌ - You are not in a voice channel and you didn't mention a voice channel.**", ephemeral=True)
        elif not voice_channel:
            voice_channel = interaction.user.voice.channel

        try:
            await interaction.response.defer(ephemeral=True)
            await voice_channel.connect(self_deaf=True, self_mute=True)
            await interaction.followup.send("**✅ - Connected to the voice channel. Now drag me to another voice channel.**")
            self.interaction: discord.Interaction = interaction
        except discord.ClientException:
            return await interaction.response.send_message("**❌ - I'am already in a voice channel drag me and I'll move everyone.**", ephemeral=True)
        
    
    @moveall.error
    async def moveall_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(title="Missing Permissions", description="⛔ - You don't have the permission to use this command.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error", description="⛔ - An error occured while running the command!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(error)            

    @tasks.loop(minutes=1)
    async def disconnect_after_inactivity(self):
        for voice_channel in self.connected_voice_channels.values():
            if voice_channel is not None:
                await voice_channel.guild.voice_client.disconnect()
                print(f"Disconnected from {voice_channel.name}")

async def setup(bot: commands.Bot):
    await bot.add_cog(MoveAll(bot))

        



        
