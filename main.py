import discord
import requests
from bs4 import BeautifulSoup
import json
import random
import yaml
import os

DISCORD_TOKEN = os.getenv('CHUNITHM_DISCORD_BOT_TOKEN')
CHUNIREC_TOKEN = os.getenv('CHUNIREC_TOKEN')
URL = f"https://api.chunirec.net/2.0/music/showall.json?id=d300c054c179990a&region=jp2&token={CHUNIREC_TOKEN}"

bot = discord.Bot(
    intents=discord.Intents.all(),
    activity=discord.Game("CHUNITHM VERSE"),
)

with open('images/jacket.yaml', mode='rb') as f:
  yml = yaml.safe_load(f)

r = requests.get(URL)
with open("./new.txt", mode='w') as f:
  json.dump(r.json(), f, indent=4)
  

title_pair = []
for music in r.json():
  title = music['meta']['title']
  level = ""
  diff = ""
  if 'ULT' in music['data']:
    level = f"{music['data']['ULT']['const']}"
    diff = "ULT"
  elif 'MAS' in music['data']:
    level = f"{music['data']['MAS']['const']}"
    diff = "MAS"
  else:
    continue
  title_pair.append(
    {
      "title": title, 
      "diff": diff,
      "level": level
    })

#起動確認
@bot.event
async def on_ready():
    print("動作を開始")

@bot.command(name="更新", description="定義ファイルを更新します。")
async def ping(ctx: discord.ApplicationContext):
  with open('images/jacket.yaml', mode='rb') as f:
    yml = yaml.safe_load(f)

  r = requests.get(URL)
  with open("./new.txt", mode='w') as f:
    json.dump(r.json(), f, indent=4)

  title_pair = []
  for music in r.json():
    title = music['meta']['title']
    level = ""
    diff = ""
    if 'ULT' in music['data']:
      level = f"{music['data']['ULT']['const']}"
      diff = "ULT"
    elif 'MAS' in music['data']:
      level = f"{music['data']['MAS']['const']}"
      diff = "MAS"
    else:
      continue
    title_pair.append(
      {
        "title": title, 
        "diff": diff,
        "level": level
    })
    
    
  #画像の更新
  res = requests.get('https://qman11010101.github.io/constant-table/chunithm.html')
  soup = BeautifulSoup(res.text, 'html.parser')
  yml = {}

  itemelms = soup.find_all('div', {'class': 'items'})
  for elm in itemelms:
    if elm.find('img') and elm.find('div', {'class': 'titleblock'}):
      uri = elm.find('img')['src']
      title_text = elm.find('div', {'class': 'titleblock'}).find('span').get_text()
      image_data = requests.get(uri).content
      filename = uri[uri.rfind('/') + 1:]
      yml[title_text] = filename
        
      with open(f'./images/{filename}', mode='wb') as f:
        f.write(image_data)
      
  with open('./images/jacket.yaml', mode='wb') as f:
    yaml.dump(yml, f, encoding='utf-8', allow_unicode=True)
  
  await ctx.respond('更新完了')
    
    

@bot.command(name="課題曲", description="譜面定数<const>の課題曲を返します。<const>=0で全曲からランダム選択")
async def ping(ctx: discord.ApplicationContext, const: float):
    if const == 0:
      rand_music = random.choice(title_pair)
      jacket = yml[rand_music['title']]
      await ctx.respond(f'{rand_music['title']} / {rand_music['diff']} / {rand_music['level']}', file=discord.File(f"./images/{jacket}"))
    else:
      spoit_title_pair = [ x for x in title_pair if float(x['level']) == const ]
      if not spoit_title_pair:
        await ctx.respond(f'譜面定数{const}の譜面は存在しません。')
      else:
        spoit_rand_music = random.choice(spoit_title_pair)
        jacket = yml[spoit_rand_music['title']]
        await ctx.respond(f'{spoit_rand_music['title']} / {spoit_rand_music['diff']} {spoit_rand_music['level']}', file=discord.File(f"./images/{jacket}"))
        
bot.run(DISCORD_TOKEN)