from discord.ext import commands
from discord import app_commands
import requests
import discord
import json

class Corona(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Returns the current corona stats of a country. Tunisia if none was mentioned.')
    @app_commands.describe(country="The country to get the corona stats of. (optional)")
    async def corona(self, interaction: discord.Interaction, country: str = 'Tunisia'):
        url = "https://covid-193.p.rapidapi.com/statistics"
        country = country.title()
        if country == 'United States':
            country = "Usa"
        querystring = {"country":country}

        headers = {
            "X-RapidAPI-Key": "ec2f8ccf8bmshbf1cf334816d19ep12966ejsnbf378abe0c43",
            "X-RapidAPI-Host": "covid-193.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        json_data = json.loads(response.text)
        if json_data['results'] == 0:
            embed = discord.Embed(description=':rolling_eyes: - {} I can\'t find a country named **{}**!'.format(interaction.user.name, country), color=0xe74c3c)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            url = "https://country-info.p.rapidapi.com/search"
            if country == 'Usa':
                country = 'United states'
            querystring = {"query":country}
            headers = {
            "X-RapidAPI-Key": "ec2f8ccf8bmshbf1cf334816d19ep12966ejsnbf378abe0c43",
            "X-RapidAPI-Host": "country-info.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)

            flag = json.loads(response.text)[0]['flag']
            embed = discord.Embed(title=f'Corona Statistics in {country} {flag}:', color=0xe74c3c)
            continent = json_data['response'][0]['continent']
            population = json_data['response'][0]['population']
            new_cases = json_data['response'][0]['cases']['new']
            active_cases = json_data['response'][0]['cases']['active']
            recovered_cases = json_data['response'][0]['cases']['recovered']
            total_cases = json_data['response'][0]['cases']['total']
            new_deaths = json_data['response'][0]['deaths']['new']
            total_deaths = json_data['response'][0]['deaths']['total']
            day = json_data['response'][0]['day']
            embed.add_field(name='Continent:', value=continent)
            embed.add_field(name='Country:', value=country)
            embed.add_field(name='Population:', value=population)
            embed.add_field(name='Total Cases:', value=total_cases)
            embed.add_field(name='Active Cases:', value=active_cases)
            embed.add_field(name='New Cases:', value=new_cases)
            embed.add_field(name='Recovered:', value=recovered_cases)
            embed.add_field(name='Total Deaths:', value=total_deaths)
            embed.add_field(name='New Deaths:', value=new_deaths)
            embed.set_author(name=day)
            embed.set_footer(text='Stay safe 🌸')
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Corona(bot))