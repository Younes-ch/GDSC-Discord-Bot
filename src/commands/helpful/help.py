from helpers.my_custom_classes import ViewForHelpCommand
from helpers.my_custom_functions import generate_embed
from discord.ext import commands
from discord import app_commands
import discord

cmds = [
            {
                'name' : '/avatar',
                'id': '1059891620549509191',
                'args' : ['[member]', ''],
                'exmp' : ['</avatar:1059891620549509191> @user', '</avatar:1059891620549509191>'],
                'dis' : 'Returns the avatar of the member mentioned or the user who invoked the command (in case no one was mentioned).'
            },
            {
                'name': '/icon',
                'id': '1058100915942473800',
                'args': [''],
                'exmp': ['</icon:1058100915942473800>'],
                'dis': 'Returns the server icon.'
            },
            {
                'name' : '/meme',
                'id': '1058100915439161407',  
                'args' : ['[subreddit name]', ''],
                'exmp': ['</meme:1058100915439161407> dankmemes', '</meme:1058100915439161407>'],
                'dis' : 'Returns a random meme from the subbredit you provided or Dankmemes/memes/me_irl (in case no Subbredit name was provided).'
            },
            { 
                'name' : '/weather',
                'id': '1058100915439161411',  
                'args' : ['[city name]', ''],
                'exmp' : ['</weather:1058100915439161411> Monastir', '</weather:1058100915439161411>'],
                'dis' : 'Returns current weather in the city mentioned or Sousse if no city was mentioned.'
            },
            {
                'name' : '/say',
                'id': '1058100915439161405',
                'args' : ['[Text Channel] [message]', '[message]'],
                'exmp': ['</say:1058100915439161405> #general Hello everyone!', '</say:1058100915439161405> Hello everyone!'],
                'dis' : 'Sends the message as the bot in the text channel provided.'
            },
            {
                'name': '&announce',
                'id': ':>',
                'args': ['[message]'],
                'exmp': ['&announce Hello everyone!'],
                'dis': 'Sends the message as the bot in the announcements channel.'
            },
            {
                "name" : '/fact',
                'id': '1058100915439161406', 
                'args' : [''],
                'exmp': ['</fact:1058100915439161406>'],
                'dis' : 'Returns a random fact.'
            },
            {
                "name" : '/corona',
                'id': '1058100915439161413', 
                'args' : ['[country name]', ''],
                'exmp': ['</corona:1058100915439161413> morocco', '</corona:1058100915439161413>'],
                'dis' : 'Returns today''s COVID-19 statistics of the mentioned country (Tunisia if none was mentioned).'
            },
            {
                "name" : '/rps',
                'id': '1058100915942473801', 
                'args' : ['[member]'],
                'exmp': ['</rps:1058100915942473801> @user'],
                'dis' : 'Creates a RPS game between you and the mentioned member.'
            },
            {
                "name" : '/joke',
                'id': '1058100915439161409', 
                'args' : ['[word]', ''],
                'exmp': ['</joke:1058100915439161409> programming', '</joke:1058100915439161409>'],
                'dis' : 'Returns a random joke contains the word (word argument can be omitted).'
            },
            {
                "name" : '/ping',
                'id': '1058100915439161408', 
                'args' : [''],
                'exmp': ['</ping:1058100915439161408>'],
                'dis' : 'Returns current bot\'s ping.'
            },
            {
                "name" : '/quote',
                'id': '1058100915439161410', 
                'args' : [''],
                'exmp': ['</quote:1058100915439161410>'],
                'dis' : 'Returns a random quote.'
            },
            {
                "name" : '/userinfo',
                'id': '1058100915942473798', 
                'args' : ['[member]', ''],
                'exmp': ['</userinfo:1058100915942473798> @user', '</userinfo:1058100915942473798>'],
                'dis' : 'Shows detailed information about the mentioned member or the user in case no one was mentioned.'
            },
            {
                "name" : '/serverinfo',
                'id': '1058100915439161412', 
                'args' : [''],
                'exmp': ['</serverinfo:1058100915439161412>'],
                'dis' : 'Shows detailed information about the server where the command was called.'
            },
            {
                "name" : "/question",
                'id': '1058100915942473803',
                "args" : ["[question]"],
                'exmp': ['</question:1058100915942473803> How to center a div?'],
                "dis" : "Fetches a similar question from stackoverflow and returns the correct answer."
            },
            {
                "name" : "/socialmedia",
                'id': '1058100915942473802',
                "args" : [""],
                'exmp': ['</socialmedia:1058100915942473802>'],
                'dis' : 'Displays our social media links.'
            },
            {
                "name" : "/snipe",
                'id' : '1058100915439161404',
                "args" : [""],
                'exmp': ['</snipe:1058100915439161404>'],
                'dis' : 'Retrieves the last deleted messages in the channel.'
            },
            {
                "name" : "/moveme",
                "id" : "1058162013806805062",
                "args" : ["[voice channel]", "[member]"],
                "exmp" : ['</moveme:1058162013806805062> #voice-channel', '</moveme:1058162013806805062> @user'],
                "dis" : "Moves you to the mentioned voice channel or the mentioned member."
            },
            {
                "name" : "/moveall",
                "id" : "1058173029852651631",
                "args" : ["[voice channel]", ""],
                "exmp" : ['</moveall:1058173029852651631> #voice-channel', '</moveall:1058173029852651631>'],
                "dis" : "The bot joins the mentioned voice channel or your voice channel if none mentioned and waits for you to drag him to another voice channel."
            },
            {
                "name" : "/setnick",
                "id" : "1058402928819441684",
                "args" : ["[member] [nickname]", "[member]"],
                "exmp" : ['</setnick:1058402928819441684> @user new nickname', '</setnick:1058402928819441684> @user'],
                "dis" : "Changes the nickname of the mentioned member back to his original nickname if no nickname was given else changes it to the given nickname."
            },
            {
                "name" : "/slowmode",
                "id" : "1058417166833176597",
                "args" : ["[text channel] [seconds]", "[seconds]", "[text channel]", ""],
                "exmp" : [
                          '</slowmode:1058417166833176597> #text-channel 10',
                          '</slowmode:1058417166833176597> 10',
                          '</slowmode:1058417166833176597> #text-channel',
                          '</slowmode:1058417166833176597>'
                        ],
                "dis" : "Sets the slowmode of the mentioned text channel to the given seconds or the current text channel if no text channel was mentioned."
            },
            {
                "name" : '/help',
                'id' : '1058100915942473804', 
                'args' : ['[command]', ''],
                'exmp': ['</help:1058100915942473804> avatar', '</help:1058100915942473804>'],
                'dis' : 'Returns the list of all commands or get help for a specific command.'
            }
        ]

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Get the list of all commands or get help for a specific command.')
    @app_commands.choices(command=[app_commands.Choice(name=cmd["name"], value=cmd["name"]) for cmd in cmds])
    @app_commands.describe(command='The command you want to get help for.')
    async def help(self, interaction: discord.Interaction, command: app_commands.Choice[str] | None):
        if command is None:
            embed1 = discord.Embed(title='Commands:', color=0x70e68a)
            embed1.set_footer(text='Requested by {}'.format(interaction.user), icon_url = interaction.user.display_avatar.url)
            embed1.set_author(name='Github Link', url='https://github.com/Younes-ch/Discord-Bot-py', icon_url='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
            embed2, embed3, embed4, embed5 = (embed1.copy() for _ in range(4))
            counter = 0
            for cmd in cmds:
                counter += 1
                if counter <= 5:
                    if "&announce" in cmd["name"]:
                        embed1.add_field(name=f'{cmd["name"]}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                    else:
                        embed1.add_field(name=f'<{cmd["name"]}:{cmd["id"]}>', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                elif counter > 5 and counter <= 10:
                    if "&announce" in cmd["name"]:
                        embed2.add_field(name=f'{cmd["name"]}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                    else:
                        embed2.add_field(name=f'<{cmd["name"]}:{cmd["id"]}>', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                elif counter > 11 and counter <= 16:
                    if "&announce" in cmd["name"]:
                        embed3.add_field(name=f'{cmd["name"]}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                    else:
                        embed3.add_field(name=f'<{cmd["name"]}:{cmd["id"]}>', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                elif counter > 16 and counter <= 21:
                    if "&announce" in cmd["name"]:
                        embed4.add_field(name=f'{cmd["name"]}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                    else:
                        embed4.add_field(name=f'<{cmd["name"]}:{cmd["id"]}>', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                else:
                    if "&announce" in cmd["name"]:
                        embed5.add_field(name=f'{cmd["name"]}:', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
                    else:
                        embed5.add_field(name=f'<{cmd["name"]}:{cmd["id"]}>', value=f'`{cmd["name"]} {" | ".join([arg for arg in cmd["args"] if arg])}` : {cmd["dis"]}', inline=False)
            listOfEmbeds = [embed1, embed2, embed3, embed4, embed5]
            await interaction.response.send_message(embed=embed1, ephemeral=True)
            view = ViewForHelpCommand(interaction=interaction, listOfEmbeds=listOfEmbeds)
            await interaction.edit_original_response(view=view)
        else:
            for cmd in cmds:
                if cmd['name'] == command.name:
                    if "&announce" in cmd["name"]:
                        embed = generate_embed(cmd["name"], cmd['dis'], interaction.user, {'usage' : [f'{cmd["name"]} {arg}' for arg in cmd['args']], 'examples' : cmd["exmp"]})
                    else:
                        embed = generate_embed(f"<{cmd['name']}:{cmd['id']}>", cmd['dis'], interaction.user, {'usage' : [f'{cmd["name"]} {arg}' for arg in cmd['args']], 'examples' : cmd["exmp"]})
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    break

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
