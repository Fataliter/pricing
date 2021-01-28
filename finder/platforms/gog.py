import requests
from bs4 import BeautifulSoup as bs

GAMES = {
    'Trine 3': ['trine_3_the_artifacts_of_power'],
    'Trine 4': ['trine_4_the_nightmare_prince', 'trine_4_melody_of_mystery']
}


class Gog:

    def __init__(self):
        self.url = 'https://www.gog.com/game/'

    def run(self):
        prices = {}
        for game, game_urls in GAMES.items():
            prices[game] = {}
            for url in game_urls:
                response = requests.get(self.url + url)
                bs_content = bs(response.text, "html.parser")
                name_from_site = bs_content.find('h1', { 'class': 'productcard-basics__title' }).getText().strip()
                prices[game][name_from_site] = {}

                purchase = bs_content.find('div', { 'class': 'product-actions-price' })

                original_price = purchase.find('span', { 'class': 'product-actions-price__base-amount' }).getText().strip()
                final_price = purchase.find('span', {'class': 'product-actions-price__final-amount'}).getText().strip()

                if original_price == final_price:
                    prices[game][name_from_site]['orig'] = {
                        'original_price': original_price
                    }
                else:
                    prices[game][name_from_site]['dsc'] = {
                        'original_price': original_price,
                        'final_price': final_price
                    }

        return prices
