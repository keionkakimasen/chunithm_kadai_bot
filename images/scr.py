import requests
from bs4 import BeautifulSoup
import yaml

res = requests.get('https://qman11010101.github.io/constant-table/chunithm.html')
soup = BeautifulSoup(res.text, 'html.parser')
yml = {}

itemelms = soup.find_all('div', {'class': 'items'})
for elm in itemelms:
  print(elm)
  if elm.find('img') and elm.find('div', {'class': 'titleblock'}):
    uri = elm.find('img')['src']
    title_text = elm.find('div', {'class': 'titleblock'}).find('span').get_text()
    image_data = requests.get(uri).content
    filename = uri[uri.rfind('/') + 1:]
    print(title_text, filename)
    yml[title_text] = filename
        
    with open(filename, mode='wb') as f:
      f.write(image_data)
      
with open('jacket.yaml', mode='wb') as f:
  yaml.dump(yml, f, encoding='utf-8', allow_unicode=True)
  
