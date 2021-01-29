import requests
from bs4 import BeautifulSoup as bs

GAMES = {
    'Trine': ['DD-TRINE-ULTIMATE-COLLECTION/trine-ultimate-colection'],
    'Trine 4': ['DD-MG-TRINE-4-THE-NIGHTMARE-PRINCE/trine-4-the-nightmare-prince']
}


class Gamersgate:

    def __init__(self):
        self.url = 'https://www.gamersgate.com/'

    def run(self):
        prices = {}
        for game, game_urls in GAMES.items():
            prices[game] = {}
            for url in game_urls:
                response = requests.get(self.url + url)
                bs_content = bs(response.text, "html.parser")
                content = bs_content.find('div', { 'id': 'PP_data_main' })

                name_from_site = content.find('div', { 'class': 'ttl' }).find('h1').getText().strip()
                prices[game][name_from_site] = { 'url': self.url + url }

                divs = content.find_all('div')
                discount = None
                for div in divs:
                    if not div.has_attr('class'):
                        discount = div
                        break

                if discount is not None:
                    prices[game][name_from_site]['dsc'] = {
                        'pct': discount.find_all('span')[-1].getText().strip().replace("\xa0", ''),
                        'original_price': discount.find('span', { 'class': 'bold white' }).getText().strip().replace("\xa0", ''),
                        'final_price': content.find('div', {'class': 'price_price'}).find('span').getText().strip().replace("\xa0", '')
                    }
                else:
                    prices[game][name_from_site]['orig'] = {
                        'original_price': content.find('div', {'class': 'price_price'}).find('span').getText().strip().replace("\xa0", '')
                    }

        return prices
