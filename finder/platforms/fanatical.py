from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs


GAMES = {
    'Trine 3': ['trine-3-the-artifacts-of-power'],
    'Trine 4': ['trine-4-the-nightmare-prince']
}


class Fanatical:

    def __init__(self):
        self.url = 'https://www.fanatical.com/en/game/'

    def run(self):
        prices = {}
        for game, game_urls in GAMES.items():
            prices[game] = {}
            for url in game_urls:
                session = HTMLSession()
                resp = session.get(self.url + url)
                resp.html.render()
                bs_content = bs(resp.html.html, "html.parser")

                name_from_site = bs_content.find('h1', { 'class': 'product-name' }).getText().strip()
                prices[game][name_from_site] = {}

                purchase = bs_content.find('div', { 'class': 'price-container' })
                discount_block = purchase.find('div', { 'class': 'was-price' })

                if discount_block is not None:
                    prices[game][name_from_site]['dsc'] = {
                        'pct': purchase.find('div', { 'class': 'saving-percentage' }).getText().strip(),
                        'original_price': discount_block.find('span').getText().strip(),
                        'final_price': purchase.find('div', { 'class': 'price' }).find('span').getText().strip()
                    }
                else:
                    prices[game][name_from_site]['orig'] = {
                        'original_price': purchase.find('div', { 'class': 'price' }).find('span').getText().strip()
                    }

        return prices
