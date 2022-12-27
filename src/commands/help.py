from helpers.my_custom_classes import ViewForHelpCommand
from helpers.my_custom_functions import generate_embed
from discord.ext import commands
from discord import app_commands
import discord

cmds = [
                {
                    'name' : '/avatar',  
                    'args' : ['[member]', ''],
                    'exmp' : ['/avatar @user', '/avatar'],
                    'dis' : 'Returns the avatar of the member mentioned or the user who invoked the command (in case no one was mentioned).'
                },
                {
                    'name': '/icon',
                    'args': [''],
                    'exmp': ['/icon'],
                    'dis': 'Returns the server icon.'
                },
                {
                    'name' : '/meme',  
                    'args' : ['[subreddit name]', ''],
                    'exmp': ['/meme dankmemes', '/meme'],
                    'dis' : 'Returns a random meme from the subbredit you provided or Dankmemes/memes/me_irl (in case no Subbredit name was provided).'
                },
                { 
                    'name' : '/weather',  
                    'args' : ['[city name]', ''],
                    'exmp' : ['/weather Monastir', '/weather'],
                    'dis' : 'Returns current weather in the city mentioned or Sousse if no city was mentioned.'
                },
                {
                    'name' : '/say',
                    'args' : ['[Text Channel] [message]', '[message]'],
                    'exmp': ['/say #general Hello everyone!', '/say Hello everyone!'],
                    'dis' : 'Sends the message as the bot in the text channel provided.'
                },
                {
                    'name': '&announce',
                    'args': ['[message]'],
                    'exmp': '&announce Hello everyone!',
                    'exmp': ['&announce Hello everyone!'],
                    'dis': 'Sends the message as the bot in the announcements channel.'
                },
                {
                    "name" : '/fact', 
                    'args' : [''],
                    'exmp': ['/fact'],
                    'dis' : 'Returns a random fact.'
                },
                {
                    "name" : '/corona', 
                    'args' : ['[country name]', ''],
                    'exmp': ['/corona morocco', '/corona'],
                    'dis' : 'Returns today''s COVID-19 statistics of the mentioned country (Tunisia if none was mentioned).'
                },
                {
                    "name" : '/rps', 
                    'args' : ['[member]'],
                    'exmp': ['/rps @user'],
                    'dis' : 'Creates a RPS game between you and the mentioned member.'
                },
                {
                    "name" : '/joke', 
                    'args' : ['[word]', ''],
                    'exmp': ['/joke programming', '/joke'],
                    'dis' : 'Returns a random joke contains the word (word argument can be omitted).'
                },
                {
                    "name" : '/ping', 
                    'args' : [''],
                    'exmp': ['/ping'],
                    'dis' : 'Returns current bot\'s ping.'
                },
                {
                    "name" : '/quote', 
                    'args' : [''],
                    'exmp': ['/quote'],
                    'dis' : 'Returns a random quote.'
                },
                {
                    "name" : '/userinfo', 
                    'args' : ['[member]', ''],
                    'exmp': ['/userinfo @user', '/userinfo'],
                    'dis' : 'Shows detailed information about the mentioned member or the user in case no one was mentioned.'
                },
                {
                    "name" : '/serverinfo', 
                    'args' : [''],
                    'exmp': ['/serverinfo'],
                    'dis' : 'Shows detailed information about the server where the command was called.'
                },
                {
                    "name" : "/question",
                    "args" : ["[question]"],
                    'exmp': ['/question How to center a div?'],
                    "dis" : "Fetches a similar question from stackoverflow and returns the correct answer."
                },
                {
                    "name" : '/help', 
                    'args' : ['[command]', ''],
                    'exmp': ['/help avatar', '/help'],
                    'dis' : 'Returns the list of all commands or get help for a specific command.'
                }
            ]


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Get the list of all commands or get help for a specific command.')
    @app_commands.choices(command=[app_commands.Choice(name=cmd['name'], value=cmd['name']) for cmd in cmds])
    @app_commands.describe(command='The command you want to get help for.')
    async def help(self, interaction: discord.Interaction, command: app_commands.Choice[str] | None):
        if command is None:
            embed1 = discord.Embed(title='Commands:', color=0x70e68a)
            embed2 = discord.Embed(title='Commands:', color=0x70e68a)
            embed3 = discord.Embed(title='Commands:', color=0x70e68a)
            embed4 = discord.Embed(title='Commands:', color=0x70e68a)
            embed1.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
            embed1.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
            embed2.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
            embed2.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
            embed3.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
            embed3.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
            embed4.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
            embed4.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
            counter = 0
            for cmd in cmds:
                counter += 1
                if counter <= 5:
                    embed1.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                elif counter > 5 and counter <= 10:
                    embed2.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                elif counter > 11 and counter <= 16:
                    embed3.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                else:
                    embed4.add_field(name=f'{cmd["name"].capitalize()}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
            listOfEmbeds = [embed1, embed2, embed3, embed4]
            await interaction.response.send_message(embed=embed1, ephemeral=True)
            view = ViewForHelpCommand(interaction=interaction, listOfEmbeds=listOfEmbeds)
            await interaction.edit_original_response(view=view)
        else:
            for cmd in cmds:
                if cmd['name'] == command.name:
                    embed = generate_embed(cmd['name'].capitalize(), cmd['dis'], interaction.user, {'usage' : [f'{cmd["name"]} {arg}' for arg in cmd['args']], 'examples' : cmd["exmp"]})
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    break

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
