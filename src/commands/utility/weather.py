from discord.ext import commands
from discord import app_commands
import requests
import discord
import json
import os

class Weather(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(description='Get the weather of a city. If no city is specified, the weather of Sousse will be displayed.')
    @app_commands.describe(city="The city to get the weather of. (optional)")
    async def weather(self, interaction: discord.Interaction, city: str = 'Sousse'):
        api_key = os.getenv('WEATHER_API_KEY')
        base_url = 'http://api.openweathermap.org/data/2.5/weather?'
        complete_url = base_url + 'appid=' + api_key + '&q=' + city.replace(' ', '+')
        response = requests.get(complete_url)
        json_data = json.loads(response.text)
        if 'message' in json_data.keys():
            embed = discord.Embed(description=f':rolling_eyes: - {interaction.user.name} I can\'t find a city named **{city}**', color = 0xe74c3c)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            country_code = json_data['sys']['country'].lower()
            city = json_data['name']
            weather_main = json_data['weather'][0]['main']
            weather_description = json_data['weather'][0]['description']
            weather_icon = 'https://openweathermap.org/img/wn/' + json_data['weather'][0]['icon'] + '@2x.png'
            temperature = str(round(json_data['main']['temp'] - 273.15, 2))
            feels_like = str(round(json_data['main']['feels_like'] - 273.15, 2))
            humidity = str(json_data['main']['humidity']) + '%'
            wind_speed = str(json_data['wind']['speed']) + 'm/s'

            embed = discord.Embed(title=f'Current weather in {city} :flag_{country_code}::', color=interaction.user.top_role.color)
            embed.add_field(name='Weather:', value=weather_main)
            embed.add_field(name='Description:', value=weather_description)
            embed.add_field(name='Temperature:', value=temperature)
            embed.add_field(name='Feels like:', value=feels_like)
            embed.add_field(name='Humidity:', value=humidity)
            embed.add_field(name='Wind speed:', value=wind_speed)
            embed.set_thumbnail(url=weather_icon)
            embed.set_footer(text=f'Requested by {interaction.user.name}', icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Weather(bot))
