import requests
from bs4 import BeautifulSoup as bs

GAMES = {
    'Trine Ultimate Collection': 'trine_ultimate_collection',
    'Trine 3: The Artifacts of Power': 'trine_3_the_artifacts_of_power',
    'Trine 4: The Nightmare Prince': 'trine_4_the_nightmare_prince',
    'Trine 4: Melody of Mystery': 'trine_4_melody_of_mystery',
    'Grim Dawn': 'grim_dawn',
    'Grim Dawn Definitive Edition': 'grim_dawn_definitive_edition'
}


class Gog:

    def __init__(self, prices):
        self.url = 'https://www.gog.com/game/'
        self.prices = prices

    def run(self):
        for game, game_url in GAMES.items():
            if game not in self.prices : self.prices[game] = []
            price_obj = {'url': self.url + game_url, 'platform': 'gog'}

            response = requests.get(self.url + game_url)
            bs_content = bs(response.text, "html.parser")

            purchase = bs_content.find('div', { 'class': 'product-actions-price' })

            original_price = purchase.find('span', { 'class': 'product-actions-price__base-amount' }).getText().strip()
            final_price = purchase.find('span', {'class': 'product-actions-price__final-amount'}).getText().strip()

            if original_price == final_price:
                price_obj['orig'] = {
                    'original_price': original_price
                }
            else:
                price_obj['dsc'] = {
                    'original_price': original_price,
                    'final_price': final_price
                }

            self.prices[game].append(price_obj)

        return self.prices
