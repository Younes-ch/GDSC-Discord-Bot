from helpers.my_custom_classes import ViewForQuestionCommand
from discord.ext import commands
from discord import app_commands
import urllib.parse
import html2text
import requests
import discord
import os

class Question(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Get the best answer to your question from StackOverflow!')
    @app_commands.describe(question="The question to search for.")
    async def question(self, interaction: discord.Interaction, question: str):
        # {
        #   "My Test Server ID": "Channel ID",
        #   "GDSC ISSATSo Community Server ID": " Channel ID",
        # }
        corresponding_channels = {
            828940910053556224: 1055489016281182360,
            783404400416391189: 1056268271323709451,
        }
        question = '"' + urllib.parse.quote(question.lower()) + '"'
        API_KEY = os.getenv('STACKOVERFLOW_API_KEY')
        if interaction.channel.id in corresponding_channels.values():
            response = requests.get(f"https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=votes&q={question}&site=stackoverflow&key={API_KEY}")
            data = response.json()

            converter = html2text.HTML2Text()

            if data["items"]:
                questions = []
                questions_id = []
                for i in range(min(5, len(data["items"]))):
                    question_title = converter.handle(data["items"][i]["title"]).strip()[:97] + "..."
                    questions.append(question_title)
                    questions_id.append(data["items"][i]["question_id"])
                view = ViewForQuestionCommand(interaction, questions, questions_id, converter)
                await interaction.response.defer()
                await interaction.followup.send(f"Here are the top 5 similar questions that I found on Stack Overflow:", view=view)
            else:
                await interaction.response.send_message("I'm sorry, I could not find any similar posted question to that question on Stack Overflow.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Please use this command in the <#{corresponding_channels[interaction.guild.id]}> channel.", ephemeral=True)
            return

    @question.error
    async def question_error(self, interaction : discord.Interaction, error: Exception):
        embed = discord.Embed(description=":no_entry: An error occurred while executing this command.", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(Question(bot))