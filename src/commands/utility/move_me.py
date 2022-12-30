from discord.ext import commands
from discord import app_commands
import discord

class MoveMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Moves you to another voice channel")
    @app_commands.describe(input="The voice channel or the member to move to")
    @app_commands.guild_only()
    async def moveme(self, interaction: discord.Interaction, input: str):
        if not interaction.user.voice:
            return await interaction.response.send_message("**You are not in a voice channel**", ephemeral=True)

        if input.startswith("<") and input.endswith(">"):
            if input.startswith("<@"):
                member = interaction.guild.get_member(int(input[2:-1]))
            else:
                channel = interaction.guild.get_member(int(input[2:-1]))
        else:
            if input.isnumeric():
                member = interaction.guild.get_member(int(input))
                channel = interaction.guild.get_channel(int(input))
            else:
                member = interaction.guild.get_member_named(input)
                try:
                    channel = interaction.guild.get_channel(list(filter(lambda vc: vc.name == input, interaction.guild.voice_channels))[0].id)
                except IndexError:
                    channel = None

        if interaction.user.voice:
            if member:
                if member.voice:
                    if interaction.user.voice.channel.id == member.voice.channel.id:
                        return await interaction.response.send_message("**✅ - You are already in that channel!**", ephemeral=True)
                    await interaction.user.move_to(member.voice.channel)
                    return await interaction.response.send_message(f"**✅ - Moved you to {member.voice.channel.mention}.**", ephemeral=True)
                else:
                    return await interaction.response.send_message("**❌ - The member is not in a voice channel.**", ephemeral=True)
            elif channel:
                if interaction.user.voice.channel.id == channel.id:
                    return await interaction.response.send_message("**✅ - You are already in that channel!**", ephemeral=True)
                await interaction.user.move_to(channel)
                return await interaction.response.send_message(f"**✅ - Moved you to {channel.mention}.**", ephemeral=True)
            else:
                return await interaction.response.send_message("**🙄 - Channel not found**", ephemeral=True)
        else:
            return await interaction.response.send_message("**❌ - You are not in a voice channel**", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(MoveMe(bot))

