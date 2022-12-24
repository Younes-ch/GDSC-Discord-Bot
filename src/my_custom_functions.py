import discord
import requests
import json

def find_invite_by_code(invite_list, code):
  for inv in invite_list:     
      if inv.code == code:
          return inv

def get_random_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  random_quote = f'{json_data[0]["q"]}|{json_data[0]["a"]}'
  return random_quote


def get_random_fact():
  response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
  json_data = json.loads(response.text)
  useless_fact = f'{json_data["text"]}'
  return useless_fact

def generate_embed(title, description, author, fields : dict, color = 0x70e68a) -> discord.Embed:
  embed = discord.Embed(title=title, description=description, color=color)
  embed.add_field(name='Usage:', value="\n".join(fields['usage']))
  embed.add_field(name='Examples:', value="\n".join(fields['examples']))
  embed.set_footer(text='Requested by {}'.format(author), icon_url=author.display_avatar.url)

  return embed