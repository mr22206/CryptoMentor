from bs4 import BeautifulSoup
import requests

# Récupère les informations détaillées d'une cryptomonnaie
def captureinfo(crypto):
    url = f'https://courscryptomonnaies.com/{crypto}/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        parent_div = soup.find('div', class_='jsx-189965733 card-ctnr card-data')
        child_divs = parent_div.find_all('div', class_='jsx-189965733 data-row')
        texts = [div.find('span', class_='').get_text() for div in child_divs]
        return texts

# Récupère l'avatar (image) et la variation de prix d'une cryptomonnaie
def avatar(crypto):
    url = f'https://courscryptomonnaies.com/{crypto}/'
    response = requests.get(url)
    if response.status_code == 200:
        gen = []
        soup = BeautifulSoup(response.content, "html.parser")
        divavatar = soup.find("div", class_="jsx-2063552482 card-ctnr card-infos")
        variation = divavatar.find("div", class_="jsx-2063552482 variation-text").find("span").text.strip()
        img_src = divavatar.find('img', class_="jsx-2063552482 coin-img")["src"]
        gen.extend([variation, img_src])
        return gen
