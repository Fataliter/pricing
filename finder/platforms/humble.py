from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

GAMES = {
    'Trine 3: The Artifacts of Power': 'trine-3-the-artifacts-of-power',
    'Trine 4: The Nightmare Prince': 'trine-4-the-nightmare-prince',
    'Trine 4: Melody of Mystery': 'trine-4-melody-of-mystery'
}


class Humble:

    def __init__(self, prices):
        self.url = 'https://www.humblebundle.com/store/'
        self.prices = prices

    def run(self):
        for game, game_url in GAMES.items():
            if game not in self.prices : self.prices[game] = []
            price_obj = {'url': self.url + game_url, 'platform': 'humble' }

            session = HTMLSession()
            resp = session.get(self.url + game_url)
            resp.html.render(timeout=25.0)
            bs_content = bs(resp.html.html, "html.parser")

            purchase = bs_content.find('div', { 'class': 'price-info' })
            original_price = purchase.find('span', { 'class': 'full-price' })

            if original_price is not None:
                price_obj['dsc'] = {
                    'pct': purchase.find('div', {'class': 'discount-amount'}).getText().strip(),
                    'original_price': original_price.getText().strip(),
                    'final_price': purchase.find('span', {'class': 'current-price'}).getText().strip()
                }
            else:
                price_obj['orig'] = {
                    'original_price': purchase.find('span', {'class': 'current-price'}).getText().strip()
                }

            self.prices[game].append(price_obj)

        return self.prices
