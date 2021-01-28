from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

GAMES = {
    'Trine 3': ['trine-3-the-artifacts-of-power'],
    'Trine 4': ['trine-4-the-nightmare-prince', 'trine-4-melody-of-mystery']
}


class Humble:

    def __init__(self):
        self.url = 'https://www.humblebundle.com/store/'

    def run(self):
        prices = {}
        for game, game_urls in GAMES.items():
            prices[game] = {}
            for url in game_urls:
                session = HTMLSession()
                resp = session.get(self.url + url)
                resp.html.render(timeout=25.0)
                bs_content = bs(resp.html.html, "html.parser")

                name_from_site = bs_content.find('h1', { 'class': 'human_name-view' }).getText().strip()
                prices[game][name_from_site] = {}

                purchase = bs_content.find('div', { 'class': 'price-info' })
                original_price = purchase.find('span', { 'class': 'full-price' })

                if original_price is not None:
                    prices[game][name_from_site]['dsc'] = {
                        'pct': purchase.find('div', {'class': 'discount-amount'}).getText().strip(),
                        'original_price': original_price.getText().strip(),
                        'final_price': purchase.find('span', {'class': 'current-price'}).getText().strip()
                    }
                else:
                    prices[game][name_from_site]['orig'] = {
                        'original_price': purchase.find('span', {'class': 'current-price'}).getText().strip()
                    }

        return prices
