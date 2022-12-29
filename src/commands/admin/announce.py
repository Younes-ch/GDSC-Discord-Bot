from discord.ext import commands
import discord

class Announce(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def announce(self, ctx: commands.Context, *, message: str = ''):
        corresponding_channels = {
            828940910053556224: 935969094652551189,
            783404400416391189: 783404401250795562,
        }
        await ctx.message.delete()
        channel = ctx.guild.get_channel(corresponding_channels[ctx.guild.id])
        if message or ctx.message.attachments:
            if message:
                await channel.send(message)

            if ctx.message.attachments:
                for img in ctx.message.attachments:
                    await channel.send(file=await img.to_file())
        else:
            raise commands.CommandError
  
    @announce.error
    async def announce_error(self, ctx : commands.Context, error : commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description=':no_entry: - **{}**, you don\'t have the required permissions to run this command!'.format(ctx.author.name), color=0xe74c3c)
            await ctx.message.delete()
            await ctx.author.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.CommandError):
            embed = discord.Embed(description=':no_entry: - **{}**, you didn\'t provide a message to send!'.format(ctx.author.name), color=0xe74c3c)
            await ctx.author.send(embed=embed, delete_after=10)
        else:
            embed = discord.Embed(title='Error', description=':no_entry: - An error occured while running this command!', color=0xe74c3c)
            await ctx.author.send(embed=embed, delete_after=10)
            print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(Announce(bot))