import requests
from bs4 import BeautifulSoup as bs

GAMES = {
    'Trine Ultimate Collection': 'DD-TRINE-ULTIMATE-COLLECTION/trine-ultimate-colection',
    'Trine 4: The Nightmare Prince': 'DD-MG-TRINE-4-THE-NIGHTMARE-PRINCE/trine-4-the-nightmare-prince'
}


class Gamersgate:

    def __init__(self, prices):
        self.url = 'https://www.gamersgate.com/'
        self.prices = prices

    def run(self):
        for game, game_url in GAMES.items():
            if game not in self.prices : self.prices[game] = []
            price_obj = {'url': self.url + game_url, 'platform': 'gamersgate' }

            response = requests.get(self.url + game_url)
            bs_content = bs(response.text, "html.parser")
            content = bs_content.find('div', { 'id': 'PP_data_main' })

            divs = content.find_all('div')
            discount = None
            for div in divs:
                if not div.has_attr('class'):
                    discount = div
                    break

            if discount is not None:
                price_obj['dsc'] = {
                    'pct': discount.find_all('span')[-1].getText().strip().replace("\xa0", ''),
                    'original_price': discount.find('span', { 'class': 'bold white' }).getText().strip().replace("\xa0", ''),
                    'final_price': content.find('div', {'class': 'price_price'}).find('span').getText().strip().replace("\xa0", '')
                }
            else:
                price_obj['orig'] = {
                    'original_price': content.find('div', {'class': 'price_price'}).find('span').getText().strip().replace("\xa0", '')
                }

            self.prices[game].append(price_obj)

        return self.prices
