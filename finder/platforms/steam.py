import requests
from bs4 import BeautifulSoup as bs

GAMES = {
    'Trine': ['bundle/12294/Trine_Ultimate_Collection/'],
    'Trine 3': ['app/319910/Trine_3_The_Artifacts_of_Power/'],
    'Trine 4': ['app/690640/Trine_4_The_Nightmare_Prince/', 'app/1444560/Trine_4_Melody_of_Mystery/'],
    'Portal 2': ['app/620/Portal_2/'],
    'Grim Dawn': ['app/219990/Grim_Dawn/', 'bundle/12695/Grim_Dawn_Definitive_Edition/'],
    'We Were Here': ['bundle/12260/We_Were_Here_Series_bundle/'],
    'We Were Here Too': ['app/677160/We_Were_Here_Too/'],
    'We Were Here Together': ['app/865360/We_Were_Here_Together/'],
    'Helldivers': ['app/394510/HELLDIVERS_Dive_Harder_Edition/'],
    'Magicka 2': ['app/238370/Magicka_2/', 'bundle/15027/Magicka_2_Complete_Collection/']
}


class Steam:

    def __init__(self):
        self.url = 'https://store.steampowered.com/'

    def run(self):
        prices = {}
        for game, game_urls in GAMES.items():
            prices[game] = {}
            for url in game_urls:
                response = requests.get(self.url + url)
                bs_content = bs(response.text, "html.parser")
                content = bs_content.find('div', { 'class': 'page_content_ctn' })
                kind = url.split('/')[0]

                if kind == 'app':
                    name_from_site = content.find('div', {'class': 'apphub_AppName'}).getText().strip()
                    prices[game][name_from_site] = { 'url': self.url + url }

                    purchases = content.find_all('div', { 'class': 'game_area_purchase_game_wrapper' })

                    purchase = purchases[0]
                    for p in purchases:
                        name = p.find('h1').getText().strip()
                        if len(name.replace('Buy ', '')) <= len(name_from_site):
                            purchase = p
                            break

                    discount_block = purchase.find('div', { 'class': 'game_purchase_discount' })

                    if discount_block is not None:
                        prices[game][name_from_site]['dsc'] = {
                            'pct': discount_block.find('div', { 'class': 'discount_pct' }).getText().strip(),
                            'original_price': discount_block.find('div', { 'class': 'discount_original_price' }).getText().strip(),
                            'final_price': discount_block.find('div', {'class': 'discount_final_price' }).getText().strip()
                        }
                    else:
                        prices[game][name_from_site]['orig'] = {
                            'original_price': purchase.find('div', { 'class': 'game_purchase_price price' }).getText().strip()
                        }
                else:
                    name_from_site = content.find('h2', {'class': 'pageheader'}).getText().strip()
                    prices[game][name_from_site] = { 'url': self.url + url }

                    purchase = content.find('div', {'class': 'game_purchase_action'})
                    discount = purchase.find('div', {'class': 'discount_pct'})

                    if discount is not None:
                        discount_prices = purchase.find('div', { 'class': 'game_purchase_discount' }).find('div', { 'class': 'discount_prices' }).find_all('div')
                        prices[game][name_from_site]['dsc'] = {
                            'pct': discount.getText().strip(),
                            'original_price': discount_prices[0].getText().strip(),
                            'final_price': discount_prices[1].getText().strip()
                        }
                    else:
                        prices[game][name_from_site]['orig'] = {
                            'original_price': purchase.find('div', { 'class': 'discount_final_price' }).getText().strip()
                        }

        return prices
