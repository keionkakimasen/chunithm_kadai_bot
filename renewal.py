import requests
from bs4 import BeautifulSoup
import yaml
import json
import os

CHUNIREC_TOKEN = os.getenv('CHUNIREC_TOKEN')
URL = f"https://api.chunirec.net/2.0/music/showall.json?id=d300c054c179990a&region=jp2&token={CHUNIREC_TOKEN}"
res = requests.get('https://qman11010101.github.io/constant-table/chunithm.html')
soup = BeautifulSoup(res.text, 'html.parser')

class MusicRenewal:
  def __init__():
    pass
  
  def renewal(self):
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
        
        #すでにある場合はスキップ
        if(os.path.exists(f'images/{filename}')):
          continue
        
        with open(f'images/{filename}', mode='wb') as f:
          f.write(image_data)
        
    with open('images/jacket.yaml', mode='wb') as f:
      yaml.dump(yml, f, encoding='utf-8', allow_unicode=True)
    return

if(__name__ == "__main__"):
  music_renewal = MusicRenewal()
  music_renewal.renewal()
  print("画像更新完了")