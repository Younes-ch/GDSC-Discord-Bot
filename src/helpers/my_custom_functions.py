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

def get_random_joke(word = None):
  if word:
    url = f'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single&contains={word}&amount=1'
  else:
    url = 'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single&amount=1'
  response = requests.get(url)
  json_data = json.loads(response.text)
  if not json_data['error']:
    joke_category = json_data['category']
    joke = json_data['joke']
    return f'{joke_category}|{joke}'
  else:
    return f'error|{json_data["causedBy"][0]}'

def get_random_meme(subreddit: str = None) -> str:
  if subreddit:
    url = f'https://meme-api.com/gimme/{subreddit.lower()}'
  else:
    url = 'https://meme-api.com/gimme'
  
  response = requests.get(url)
  json_data = json.loads(response.text)
  if 'subreddit' in json_data:
    if json_data['nsfw']:
      return 'nsfw|This meme is NSFW.'
    meme_title = json_data['title']
    meme_url = json_data['url']
    meme_subreddit = '/r/' + json_data['subreddit']
    meme_upvotes = json_data['ups']
    meme_post_link = json_data['postLink']
    meme_post_author = json_data['author']
    return f'{meme_title}|{meme_url}|{meme_subreddit}|{meme_upvotes}|{meme_post_link}|{meme_post_author}'
  else:
    return f'error|{json_data["message"]}'

def generate_embed(title, description, author, fields : dict, color = 0x70e68a) -> discord.Embed:
  embed = discord.Embed(title=title, description=description, color=color)
  embed.add_field(name='Usage:', value="\n".join(fields['usage']))
  embed.add_field(name='Examples:', value="\n".join(fields['examples']))
  embed.set_footer(text='Requested by {}'.format(author), icon_url=author.display_avatar.url)

  return embed