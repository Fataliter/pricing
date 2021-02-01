from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs


GAMES = {
    'Trine 3: The Artifacts of Power': 'trine-3-the-artifacts-of-power',
    'Trine 4: The Nightmare Prince': 'trine-4-the-nightmare-prince'
}


class Fanatical:

    def __init__(self, prices):
        self.url = 'https://www.fanatical.com/en/game/'
        self.prices = prices

    def run(self):
        for game, game_url in GAMES.items():
            if game not in self.prices : self.prices[game] = []
            price_obj = {'url': self.url + game_url, 'platform': 'fanatical' }

            session = HTMLSession()
            resp = session.get(self.url + game_url)
            resp.html.render()
            bs_content = bs(resp.html.html, "html.parser")

            purchase = bs_content.find('div', { 'class': 'price-container' })
            discount_block = purchase.find('div', { 'class': 'was-price' })

            if discount_block is not None:
                price_obj['dsc'] = {
                    'pct': purchase.find('div', { 'class': 'saving-percentage' }).getText().strip(),
                    'original_price': discount_block.find('span').getText().strip(),
                    'final_price': purchase.find('div', { 'class': 'price' }).find('span').getText().strip()
                }
            else:
                price_obj['orig'] = {
                    'original_price': purchase.find('div', { 'class': 'price' }).find('span').getText().strip()
                }

            self.prices[game].append(price_obj)

        return self.prices
